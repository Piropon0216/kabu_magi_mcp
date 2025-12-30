"""
JQuants APIクライアント (MVP版)
シンプルで最小限の機能に絞った実装
"""
import os
import logging
import json
from pathlib import Path
from datetime import datetime, timedelta
import jquantsapi
import requests
from typing import Optional


class JQuantsAPIClient:
    """JQuants APIクライアント"""
    
    def __init__(self, refresh_token: Optional[str] = None, mail_address: Optional[str] = None, password: Optional[str] = None, logger: Optional[logging.Logger] = None):
        """
        初期化

        Args:
            refresh_token: リフレッシュトークン（優先）
            mail_address: メールアドレス（refresh_token が未指定の場合に使用可能）
            password: パスワード（mail_address と併用）
            logger: ロガー（Noneの場合はデフォルトロガーを使用）
        """
        self.logger = logger or logging.getLogger(__name__)
        self.client = None

        # 優先順: 引数 refresh_token -> 引数 mail/password -> 環境/.env/トークンファイル
        self.refresh_token = refresh_token
        if not self.refresh_token:
            if mail_address and password:
                self.logger.info("コンストラクタの引数 mail_address/password からリフレッシュトークンを取得します")
                self.refresh_token = self._get_refresh_token_from_credentials(mail_address, password)
            else:
                self.refresh_token = self._load_refresh_token()

        self._initialize_client()
    
    def _get_refresh_token_from_credentials(self, mail_address: str, password: str) -> str:
        """
        メールアドレスとパスワードからリフレッシュトークンを取得
        
        Args:
            mail_address: メールアドレス
            password: パスワード
        
        Returns:
            リフレッシュトークン
        """
        try:
            self.logger.info("メールアドレスとパスワードからリフレッシュトークンを取得します")
            data = {"mailaddress": mail_address, "password": password}
            base = os.environ.get("JQUANTS_API_BASE", "https://api.jquants.com")
            url = f"{base.rstrip('/')}/v1/token/auth_user"
            r_post = requests.post(
                url,
                json=data,
                timeout=10
            )
            r_post.raise_for_status()
            response = r_post.json()
            
            if "refreshToken" not in response:
                self.logger.error(f"APIレスポンスに 'refreshToken' がありません: {response}")
                raise ValueError("APIレスポンスに 'refreshToken' がありません")
            
            self.logger.info("リフレッシュトークンを正常に取得しました")
            return response["refreshToken"]
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP エラー: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"リフレッシュトークン取得エラー: {str(e)}")
            raise
    
    def _load_env_file(self):
        """
        .envファイルを読み込む
        
        Returns:
            dict: 環境変数の辞書
        """
        env_vars = {}
        env_file = Path.cwd() / ".env"
        
        if env_file.exists():
            with open(env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        env_vars[key.strip()] = value.strip()
        return env_vars
    
    def _load_refresh_token(self) -> str:
        """リフレッシュトークンを読み込む"""
        # 環境変数から直接（空文字は無視）
        env_token = os.environ.get('JQUANTS_REFRESH_TOKEN') or os.environ.get('JQUANTS_API_REFRESH_TOKEN')
        if env_token:
            self.logger.info("環境変数からリフレッシュトークンを読み込みました")
            return env_token.strip()
        
        # .envファイルから読み込み
        env_vars = self._load_env_file()
        
        # .envにリフレッシュトークンがある場合
        if 'JQUANTS_REFRESH_TOKEN' in env_vars:
            self.logger.info(".envファイルからリフレッシュトークンを読み込みました")
            return env_vars['JQUANTS_REFRESH_TOKEN']
        
        # .envにメールアドレスとパスワードがある場合（変数名の揺れを吸収）
        mail_address = env_vars.get('JQUANTS_MAIL_ADDRESS') or env_vars.get('JQUANTS_EMAIL') or os.environ.get('JQUANTS_MAIL_ADDRESS') or os.environ.get('JQUANTS_EMAIL')
        password = env_vars.get('JQUANTS_PASSWORD') or os.environ.get('JQUANTS_PASSWORD')
        if mail_address and password:
            password = env_vars['JQUANTS_PASSWORD']
            self.logger.info(".envまたは環境変数からメールアドレスとパスワードを読み込みました")
            return self._get_refresh_token_from_credentials(mail_address, password)
        
        # プロジェクトルートのファイルから（後方互換性）
        token_file = Path("/workspaces/jqapi_ETL/jquantsapi-key.txt")
        if token_file.exists():
            with open(token_file, "r") as f:
                token = f.read().strip()
            self.logger.info("ファイルからリフレッシュトークンを読み込みました")
            return token
        
        raise ValueError(
            "認証情報が設定されていません。\n"
            ".envファイルに JQUANTS_MAIL_ADDRESS と JQUANTS_PASSWORD を設定するか、\n"
            "JQUANTS_REFRESH_TOKEN を設定してください。"
        )
    
    def _initialize_client(self):
        """APIクライアントを初期化"""
        try:
            self.client = jquantsapi.Client(refresh_token=self.refresh_token)
            self.logger.info("JQuants APIクライアントを初期化しました")
        except Exception as e:
            self.logger.error(f"APIクライアント初期化エラー: {str(e)}")
            raise
    
    def get_stock_list(self):
        """
        銘柄一覧を取得
        
        Returns:
            pd.DataFrame: 銘柄一覧データ
        """
        try:
            self.logger.info("銘柄一覧の取得を開始します")
            df = self.client.get_list()
            self.logger.info(f"銘柄一覧を取得しました（{len(df)}件）")
            return df
        except Exception as e:
            self.logger.error(f"銘柄一覧取得エラー: {str(e)}")
            raise
    
    def get_stock_prices(self, start_date: str, end_date: str, code: Optional[str] = None):
        """
        株価データを取得
        
        Args:
            start_date: 開始日 (YYYYMMDD形式)
            end_date: 終了日 (YYYYMMDD形式)
            code: 銘柄コード（Noneの場合は全銘柄）
        
        Returns:
            pd.DataFrame: 株価データ
        """
        try:
            self.logger.info(f"株価データの取得を開始します（{start_date} - {end_date}）")
            
            if code:
                df = self.client.get_price_range(
                    start_dt=start_date,
                    end_dt=end_date,
                    code=code
                )
            else:
                df = self.client.get_price_range(
                    start_dt=start_date,
                    end_dt=end_date
                )
            
            self.logger.info(f"株価データを取得しました（{len(df)}件）")
            return df
        except Exception as e:
            self.logger.error(f"株価データ取得エラー: {str(e)}")
            raise
    
    def get_statements(self, code: Optional[str] = None):
        """
        財務諸表データを取得
        
        Args:
            code: 銘柄コード（Noneの場合は全銘柄）
        
        Returns:
            pd.DataFrame: 財務諸表データ
        """
        try:
            self.logger.info("財務諸表データの取得を開始します")
            
            if code:
                df = self.client.get_statements(code=code)
            else:
                df = self.client.get_statements()
            
            self.logger.info(f"財務諸表データを取得しました（{len(df)}件）")
            return df
        except Exception as e:
            self.logger.error(f"財務諸表データ取得エラー: {str(e)}")
            raise
    
    # =====================================================================
    # Phase 3.1: Standard Plan Market Statistics APIs
    # =====================================================================
    
    def get_trades_spec(self, start_date: Optional[str] = None, end_date: Optional[str] = None, code: Optional[str] = None):
        """
        投資部門別売買データを取得
        
        Args:
            start_date: 開始日 (YYYYMMDD形式、Noneの場合は直近データ)
            end_date: 終了日 (YYYYMMDD形式、Noneの場合は直近データ)
            code: 銘柄コード（Noneの場合は全銘柄）
        
        Returns:
            pd.DataFrame: 投資部門別売買データ
        """
        try:
            self.logger.info("投資部門別売買データの取得を開始します")
            
            # jquantsapi.Clientに trades_spec メソッドが存在するか確認
            # 存在しない場合は requests で直接取得
            if hasattr(self.client, 'get_trades_spec'):
                df = self.client.get_trades_spec(
                    start_dt=start_date,
                    end_dt=end_date,
                    code=code
                )
            else:
                # 直接APIを呼び出す（フォールバック）
                id_token = self.client.get_id_token()
                params = {}
                if start_date:
                    params['from'] = start_date
                if end_date:
                    params['to'] = end_date
                if code:
                    params['code'] = code
                
                response = requests.get(
                    "https://api.jquants.com/v1/markets/trades_spec",
                    headers={"Authorization": f"Bearer {id_token}"},
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()
                
                if "trades_spec" not in data:
                    raise ValueError("APIレスポンスに 'trades_spec' がありません")
                
                import pandas as pd
                df = pd.DataFrame(data["trades_spec"])
                
                # 日付列の型変換
                if "Date" in df.columns:
                    df["Date"] = pd.to_datetime(df["Date"])
            
            self.logger.info(f"投資部門別売買データを取得しました（{len(df)}件）")
            return df
        except Exception as e:
            self.logger.error(f"投資部門別売買データ取得エラー: {str(e)}")
            raise
    
    def get_weekly_margin_interest(self, start_date: Optional[str] = None, end_date: Optional[str] = None, code: Optional[str] = None):
        """
        信用取引週末残高データを取得
        
        Args:
            start_date: 開始日 (YYYYMMDD形式、Noneの場合は直近データ)
            end_date: 終了日 (YYYYMMDD形式、Noneの場合は直近データ)
            code: 銘柄コード（Noneの場合は全銘柄）
        
        Returns:
            pd.DataFrame: 信用取引週末残高データ
        """
        try:
            self.logger.info("信用取引週末残高データの取得を開始します")
            
            # jquantsapi.Clientに weekly_margin_interest メソッドが存在するか確認
            if hasattr(self.client, 'get_weekly_margin_interest'):
                df = self.client.get_weekly_margin_interest(
                    start_dt=start_date,
                    end_dt=end_date,
                    code=code
                )
            else:
                # 直接APIを呼び出す（フォールバック）
                id_token = self.client.get_id_token()
                params = {}
                if start_date:
                    params['from'] = start_date
                if end_date:
                    params['to'] = end_date
                if code:
                    params['code'] = code
                
                response = requests.get(
                    "https://api.jquants.com/v1/markets/weekly_margin_interest",
                    headers={"Authorization": f"Bearer {id_token}"},
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()
                
                # レスポンスキーは margin_interest または weekly_margin_interest の可能性
                response_key = None
                for key in ["weekly_margin_interest", "margin_interest", "weekly_margin"]:
                    if key in data:
                        response_key = key
                        break
                
                if not response_key:
                    raise ValueError(f"APIレスポンスに想定キーがありません: {list(data.keys())}")
                
                import pandas as pd
                df = pd.DataFrame(data[response_key])
                
                # 日付列の型変換
                if "Date" in df.columns:
                    df["Date"] = pd.to_datetime(df["Date"])
            
            self.logger.info(f"信用取引週末残高データを取得しました（{len(df)}件）")
            return df
        except Exception as e:
            self.logger.error(f"信用取引週末残高データ取得エラー: {str(e)}")
            raise
    
    def get_short_selling(self, start_date: Optional[str] = None, end_date: Optional[str] = None, sector: Optional[str] = None):
        """
        業種別空売り比率データを取得
        
        Args:
            start_date: 開始日 (YYYYMMDD形式、Noneの場合は直近データ)
            end_date: 終了日 (YYYYMMDD形式、Noneの場合は直近データ)
            sector: 業種名（Noneの場合は全業種）
        
        Returns:
            pd.DataFrame: 業種別空売り比率データ
        """
        try:
            self.logger.info("業種別空売り比率データの取得を開始します")
            
            # jquantsapi.Clientに short_selling メソッドが存在するか確認
            if hasattr(self.client, 'get_short_selling'):
                df = self.client.get_short_selling(
                    start_dt=start_date,
                    end_dt=end_date,
                    sector=sector
                )
            else:
                # 直接APIを呼び出す（フォールバック）
                id_token = self.client.get_id_token()
                params = {}
                if start_date:
                    params['from'] = start_date
                if end_date:
                    params['to'] = end_date
                if sector:
                    params['sector'] = sector
                
                response = requests.get(
                    "https://api.jquants.com/v1/markets/short_selling",
                    headers={"Authorization": f"Bearer {id_token}"},
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()
                
                if "short_selling" not in data:
                    raise ValueError("APIレスポンスに 'short_selling' がありません")
                
                import pandas as pd
                df = pd.DataFrame(data["short_selling"])
                
                # 日付列の型変換
                if "Date" in df.columns:
                    df["Date"] = pd.to_datetime(df["Date"])
            
            self.logger.info(f"業種別空売り比率データを取得しました（{len(df)}件）")
            return df
        except Exception as e:
            self.logger.error(f"業種別空売り比率データ取得エラー: {str(e)}")
            raise
    
    def get_short_selling_positions(self, start_date: Optional[str] = None, end_date: Optional[str] = None, code: Optional[str] = None):
        """
        空売り残高報告データを取得
        
        Args:
            start_date: 開始日 (YYYYMMDD形式、Noneの場合は直近データ)
            end_date: 終了日 (YYYYMMDD形式、Noneの場合は直近データ)
            code: 銘柄コード（Noneの場合は全銘柄）
        
        Returns:
            pd.DataFrame: 空売り残高報告データ
        """
        try:
            self.logger.info("空売り残高報告データの取得を開始します")
            
            # jquantsapi.Clientに short_selling_positions メソッドが存在するか確認
            if hasattr(self.client, 'get_short_selling_positions'):
                df = self.client.get_short_selling_positions(
                    start_dt=start_date,
                    end_dt=end_date,
                    code=code
                )
            else:
                # 直接APIを呼び出す（フォールバック）
                id_token = self.client.get_id_token()
                params = {}
                if start_date:
                    params['from'] = start_date
                if end_date:
                    params['to'] = end_date
                if code:
                    params['code'] = code
                
                response = requests.get(
                    "https://api.jquants.com/v1/markets/short_selling_positions",
                    headers={"Authorization": f"Bearer {id_token}"},
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()
                
                # レスポンスキーは short_selling_positions または short_positions の可能性
                response_key = None
                for key in ["short_selling_positions", "short_positions", "positions"]:
                    if key in data:
                        response_key = key
                        break
                
                if not response_key:
                    raise ValueError(f"APIレスポンスに想定キーがありません: {list(data.keys())}")
                
                import pandas as pd
                df = pd.DataFrame(data[response_key])
                
                # 日付列の型変換
                if "Date" in df.columns:
                    df["Date"] = pd.to_datetime(df["Date"])
            
            self.logger.info(f"空売り残高報告データを取得しました（{len(df)}件）")
            return df
        except Exception as e:
            self.logger.error(f"空売り残高報告データ取得エラー: {str(e)}")
            raise
    
    # =====================================================================
    # Phase 3.2: 未実装 Standard Plan API
    # =====================================================================
    
    def get_announcement(self, code: Optional[str] = None):
        """
        決算発表予定日データを取得
        
        Standard Plan API: /v1/fins/announcement
        
        Args:
            code: 銘柄コード（Noneの場合は全銘柄）
        
        Returns:
            pd.DataFrame: 決算発表予定日データ
        """
        try:
            self.logger.info("決算発表予定日データの取得を開始します")
            
            # jquantsapi.Clientに announcement メソッドが存在するか確認
            if hasattr(self.client, 'get_announcement'):
                df = self.client.get_announcement(code=code)
            else:
                # 直接APIを呼び出す（フォールバック）
                id_token = self.client.get_id_token()
                params = {}
                if code:
                    params['code'] = code
                
                response = requests.get(
                    "https://api.jquants.com/v1/fins/announcement",
                    headers={"Authorization": f"Bearer {id_token}"},
                    params=params,
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()
                
                if "announcement" not in data:
                    raise ValueError("APIレスポンスに 'announcement' がありません")
                
                import pandas as pd
                df = pd.DataFrame(data["announcement"])
                
                # 日付列の型変換
                for date_col in ["Date", "AnnouncementDate"]:
                    if date_col in df.columns:
                        df[date_col] = pd.to_datetime(df[date_col])
            
            self.logger.info(f"決算発表予定日データを取得しました（{len(df)}件）")
            return df
        except Exception as e:
            self.logger.error(f"決算発表予定日データ取得エラー: {str(e)}")
            raise
