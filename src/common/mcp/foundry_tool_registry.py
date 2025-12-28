"""
Foundry Tool Registry for managing Microsoft Foundry Tool Catalog integrations.

This module provides a unified interface to access tools from the Foundry Tool Catalog,
making it reusable across different domains (stock analysis, real estate, medical diagnosis, etc.).
"""

from typing import Any, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class FoundryConfig(BaseSettings):
    """
    Microsoft Foundry 接続設定
    
    環境変数から読み込み:
        FOUNDRY_ENDPOINT: Azure Foundry エンドポイント
        FOUNDRY_API_KEY: API キー
        FOUNDRY_DEPLOYMENT: モデルデプロイメント名
        FOUNDRY_API_VERSION: API バージョン
    """
    FOUNDRY_ENDPOINT: str
    FOUNDRY_API_KEY: str
    FOUNDRY_DEPLOYMENT: str = "gpt-4o"
    FOUNDRY_API_VERSION: str = "2024-10-01-preview"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
    # 後方互換性のためのエイリアス
    @property
    def foundry_endpoint(self) -> str:
        return self.FOUNDRY_ENDPOINT
    
    @property
    def foundry_api_key(self) -> str:
        return self.FOUNDRY_API_KEY
    
    @property
    def foundry_deployment(self) -> str:
        return self.FOUNDRY_DEPLOYMENT
    
    @property
    def foundry_api_version(self) -> str:
        return self.FOUNDRY_API_VERSION


class FoundryToolRegistry:
    """
    Microsoft Foundry Tool Catalog からツールを管理する汎用レジストリ
    
    Phase 1: Morningstar MCP Server (Foundry Tool Catalog から直接利用)
    Phase 2: Yahoo Finance (npm MCP Server - カスタムアダプタ経由)
    Phase 3: DuckDB, Azure Docs など
    
    使用例:
        >>> registry = FoundryToolRegistry()
        >>> morningstar_tool = registry.get_tool("morningstar")
        >>> tools = registry.get_tools_for_agent("Melchior")
    """
    
    def __init__(self, config: Optional[FoundryConfig] = None):
        """
        Initialize the Foundry Tool Registry
        
        Args:
            config: Foundry configuration. If None, loads from environment variables.
        """
        self.config = config or FoundryConfig()
        self._tool_cache: dict[str, Any] = {}
    
    def get_tool(self, tool_name: str) -> Any:
        """
        Foundry Tool Catalog からツールを取得
        
        Phase 1 では Morningstar のみサポート。
        Agent Framework が Foundry Portal で設定されたツールを自動的に利用可能にする。
        
        Args:
            tool_name: ツール名 (例: "morningstar")
        
        Returns:
            Tool instance (Agent Framework 互換)
        
        Raises:
            ValueError: サポートされていないツール名
        
        Note:
            実際の Foundry Tool 統合は Agent Framework が自動処理するため、
            Phase 1 では最小限の実装のみ。Phase 2 で Azure SDK 統合を追加予定。
        """
        if tool_name in self._tool_cache:
            return self._tool_cache[tool_name]
        
        # Phase 1: Placeholder implementation
        # Agent Framework が Foundry Portal の設定を自動的に読み込むため、
        # ここでは tool_name の検証のみ実施
        supported_tools = ["morningstar"]  # Phase 1 MVP
        
        if tool_name not in supported_tools:
            raise ValueError(
                f"Unsupported tool: {tool_name}. "
                f"Supported tools in Phase 1: {', '.join(supported_tools)}"
            )
        
        # Phase 2 で Azure SDK による実際の Tool 取得ロジックを実装予定
        # 現在は Foundry Portal での GUI 設定に依存
        tool_placeholder = {
            "name": tool_name,
            "description": f"{tool_name.capitalize()} tool from Foundry Catalog",
            "phase": "1-mvp"
        }
        
        self._tool_cache[tool_name] = tool_placeholder
        return tool_placeholder
    
    def get_tools_for_agent(self, agent_name: str) -> list[Any]:
        """
        特定エージェント用のツールリストを取得
        
        Args:
            agent_name: エージェント名 (例: "Melchior", "Balthasar", "Casper")
        
        Returns:
            ツールリスト
        
        Phase 1 MVP:
            - Melchior: [morningstar]
        
        Phase 2:
            - Balthasar: [morningstar, yahoo-finance, azure-docs]
            - Casper: [morningstar, yahoo-finance]
        """
        # Phase 1: Melchior のみ
        agent_tool_mapping = {
            "Melchior": ["morningstar"],
            # Phase 2 で追加:
            # "Balthasar": ["morningstar", "yahoo-finance", "azure-docs"],
            # "Casper": ["morningstar", "yahoo-finance"],
        }
        
        tool_names = agent_tool_mapping.get(agent_name, [])
        return [self.get_tool(name) for name in tool_names]
    
    def list_available_tools(self) -> list[str]:
        """
        利用可能なツール名のリストを取得
        
        Returns:
            ツール名リスト
        """
        return ["morningstar"]  # Phase 1 MVP


# エクスポート
__all__ = ["FoundryToolRegistry", "FoundryConfig"]
