import os

import pytest


@pytest.fixture(autouse=True, scope="function")
def filter_and_set_foundry_env_vars(monkeypatch):
    """
    各テスト関数の直前でFOUNDRY_で始まる環境変数のみをos.environに残し、
    テスト用の値を必ずセットする。
    """
    print("[DEBUG] os.environ before filtering:")
    for k, v in os.environ.items():
        print(f"  {k}={v}")
    original_env = os.environ.copy()

    # Allow preserving the real environment for live integration runs
    # If FOUNDRY_PRESERVE_ENV is set to '1', do not override FOUNDRY_* vars.
    if os.environ.get("FOUNDRY_PRESERVE_ENV") == "1":
        print("[DEBUG] FOUNDRY_PRESERVE_ENV=1 — skipping env filtering")
        yield
        # restore nothing because we didn't modify env
        return

    # FOUNDRY_ で始まるもの以外を削除
    keys_to_remove = [k for k in os.environ if not k.startswith("FOUNDRY_")]
    for k in keys_to_remove:
        monkeypatch.delenv(k, raising=False)
    # テスト用のFOUNDRY_変数を常にセット
    os.environ["FOUNDRY_ENDPOINT"] = "https://test.foundry.azure.com"
    os.environ["FOUNDRY_API_KEY"] = "test_api_key_12345"
    os.environ["FOUNDRY_DEPLOYMENT"] = "gpt-4o-test"
    os.environ["FOUNDRY_API_VERSION"] = "2024-12-01"
    print("[DEBUG] os.environ after filtering:")
    for k, v in os.environ.items():
        print(f"  {k}={v}")
    yield
    # テスト後に元の環境変数に戻す
    for k in list(os.environ.keys()):
        monkeypatch.delenv(k, raising=False)
    for k, v in original_env.items():
        monkeypatch.setenv(k, v)
