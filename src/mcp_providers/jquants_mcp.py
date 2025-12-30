import importlib
import os
import traceback
from datetime import datetime, timedelta
from typing import Any

from fastapi import FastAPI, HTTPException

# Prefer to use the official jquantsapi client when available, otherwise fall back to sample.client
try:
    jquantsapi = importlib.import_module("jquantsapi")
except Exception:
    jquantsapi = None

try:
    from sample.client import JQuantsAPIClient  # fallback
except Exception:
    JQuantsAPIClient = None


def _load_project_dotenv():
    """Load a .env file from project root (Path.cwd()) into os.environ for missing keys."""
    from pathlib import Path

    env_path = Path.cwd() / ".env"
    if not env_path.exists():
        return

    try:
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                # Only set if not already present
                if k not in os.environ:
                    os.environ[k] = v
    except Exception:
        # ignore failures to read dotenv
        pass


# Load .env at import time so uvicorn process inherits credentials from project root
_load_project_dotenv()

app = FastAPI(title="JQuants MCP PoC")


def _build_jquants_client() -> JQuantsAPIClient:
    """Construct JQuantsAPIClient using available env settings.

    Priority: JQUANTS_REFRESH_TOKEN -> (JQUANTS_MAIL_ADDRESS + JQUANTS_PASSWORD) -> raise
    """
    refresh = os.environ.get("JQUANTS_REFRESH_TOKEN") or os.environ.get("JQUANTS_API_REFRESH_TOKEN")
    mail = (os.environ.get("JQUANTS_MAIL_ADDRESS") or os.environ.get("JQUANTS_EMAIL") or os.environ.get("JQUANTS_API_MAIL_ADDRESS"))
    password = os.environ.get("JQUANTS_PASSWORD") or os.environ.get("JQUANTS_API_PASSWORD")

    # If official client is available, prefer it
    if jquantsapi is not None:
        # prefer direct constructor with mail/password if provided
        if mail and password:
            try:
                return jquantsapi.Client(mail_address=mail, password=password)
            except Exception as e:
                # if direct constructor fails, try refresh token flow
                print(f"jquantsapi.Client(mail,password) init failed: {e}")

        # ensure we have a refresh token (obtain via auth endpoint if needed)
        if not refresh and mail and password:
            base = os.environ.get("JQUANTS_API_BASE", "https://api.jquants.com")
            refresh = _get_refresh_token_via_http(base, mail, password)

        if refresh:
            try:
                return jquantsapi.Client(refresh_token=refresh)
            except Exception as e:
                # fall through to fallback client
                print(f"jquantsapi.Client(refresh) init failed: {e}")

    # Fallback to sample client if present
    if JQuantsAPIClient is not None:
        if refresh:
            return JQuantsAPIClient(refresh_token=refresh)
        if mail and password:
            return JQuantsAPIClient(mail_address=mail, password=password)

    raise RuntimeError("No JQuants credentials or client available: set JQUANTS_REFRESH_TOKEN or JQUANTS_MAIL_ADDRESS + JQUANTS_PASSWORD and install jquantsapi or keep sample client")


def _get_refresh_token_via_http(base: str, mail: str, password: str) -> str:
    """Obtain refresh token via HTTP auth endpoint (used when official client not handling auth)."""
    import requests

    url = base.rstrip("/") + "/v1/token/auth_user"
    payload = {"mailaddress": mail, "password": password}
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()
    j = r.json()
    token = j.get("refreshToken") or j.get("refresh_token")
    if not token:
        raise RuntimeError(f"no refresh token in auth response: {j}")
    return token


@app.get("/tools/jquants/price/{ticker}")
def get_price(ticker: str) -> Any:
    """Return minimal stock price info for MVP via `JQuantsAPIClient.get_stock_prices`.

    This returns a small JSON: {ticker, price, raw} where `price` is best-effort.
    """
    # normalize ticker for JQuants (e.g., '7203.T' -> '7203')
    code = str(ticker).split('.')[0]

    try:
        client = _build_jquants_client()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Use a small date range to request latest price. Use YYYYMMDD format expected by sample client.
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=5)
    start = yesterday.strftime("%Y%m%d")
    end = today.strftime("%Y%m%d")

    try:
        # normalize calls across different client implementations
        if hasattr(client, "get_stock_prices"):
            data = client.get_stock_prices(start_date=start, end_date=end, code=code)
        elif hasattr(client, "get_price_range"):
            # Official client: prefer get_prices_daily_quotes for a single code when available
            if hasattr(client, "get_prices_daily_quotes"):
                try:
                    data = client.get_prices_daily_quotes(code=code, from_yyyymmdd=start, to_yyyymmdd=end)
                except TypeError:
                    # fallback to datetime conversion if needed
                    from dateutil import tz

                    tz_tokyo = tz.gettz("Asia/Tokyo")
                    sd = datetime.strptime(start, "%Y%m%d").replace(tzinfo=tz_tokyo)
                    ed = datetime.strptime(end, "%Y%m%d").replace(tzinfo=tz_tokyo)
                    data = client.get_prices_daily_quotes(code=code, from_yyyymmdd=sd, to_yyyymmdd=ed)
            else:
                # get_price_range returns all codes; filter by Code column if present
                try:
                    df = client.get_price_range(start_dt=start, end_dt=end)
                except TypeError:
                    from dateutil import tz

                    tz_tokyo = tz.gettz("Asia/Tokyo")
                    sd = datetime.strptime(start, "%Y%m%d").replace(tzinfo=tz_tokyo)
                    ed = datetime.strptime(end, "%Y%m%d").replace(tzinfo=tz_tokyo)
                    df = client.get_price_range(start_dt=sd, end_dt=ed)

                # filter
                try:
                    data = df[df["Code"].astype(str) == str(code)]
                except Exception:
                    data = df
        else:
            # fallback: try to call a generic 'get_price' or raise
            if hasattr(client, "get_price"):
                data = client.get_price(ticker)
            else:
                raise RuntimeError("client has no supported price API")
    except Exception as e:
        detail = f"upstream error: {e}"
        # include traceback in logs for debugging
        try:
            print(traceback.format_exc())
        except Exception:
            pass
        raise HTTPException(status_code=502, detail=detail)

    # Try to extract a numeric price in a best-effort way
    price = None
    raw = data
    try:
        # If pandas DataFrame
        import pandas as pd

        if isinstance(data, pd.DataFrame):
            if not data.empty:
                # common column names: Close, close, AdjClose, adjClose, price
                for col in ["Close", "close", "AdjClose", "adjClose", "price"]:
                    if col in data.columns:
                        price = float(data.iloc[-1][col])
                        break
                # fallback: take last numeric value from last row
                if price is None:
                    last = data.iloc[-1]
                    for v in last.values:
                        if isinstance(v, (int, float)):
                            price = float(v)
                            break
    except Exception:
        # pandas may not be installed or parsing failed — ignore
        price = None

    # Ensure raw is JSON-serializable (convert pandas DataFrame to records)
    try:
        import pandas as pd

        if isinstance(raw, pd.DataFrame):
            raw = raw.tail(20).to_dict(orient="records")
    except Exception:
        pass

    result = {"ticker": ticker, "price": price, "raw": raw}
    return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8081)))
