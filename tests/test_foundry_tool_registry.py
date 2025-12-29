"""
Unit tests for Foundry Tool Registry
"""


import pytest

from src.common.mcp.foundry_tool_registry import FoundryConfig, FoundryToolRegistry


@pytest.fixture
def mock_env_vars(monkeypatch):
    """環境変数をモック"""
    monkeypatch.setenv("FOUNDRY_ENDPOINT", "https://test.foundry.azure.com")
    monkeypatch.setenv("FOUNDRY_API_KEY", "test_api_key_12345")
    monkeypatch.setenv("FOUNDRY_DEPLOYMENT", "gpt-4o-test")
    monkeypatch.setenv("FOUNDRY_API_VERSION", "2024-12-01")


def test_foundry_config_from_env(mock_env_vars):
    """FoundryConfig が環境変数から正しく読み込まれるかテスト"""
    config = FoundryConfig()

    assert config.foundry_endpoint == "https://test.foundry.azure.com"
    assert config.foundry_api_key == "test_api_key_12345"
    assert config.foundry_deployment == "gpt-4o-test"
    assert config.foundry_api_version == "2024-12-01"


def test_foundry_tool_registry_initialization(mock_env_vars):
    """FoundryToolRegistry の初期化テスト"""
    registry = FoundryToolRegistry()

    assert registry.config.foundry_endpoint == "https://test.foundry.azure.com"
    assert registry._tool_cache == {}


def test_get_tool_morningstar_phase1(mock_env_vars):
    """Phase 1: Morningstar tool 取得テスト (プレースホルダー)"""
    registry = FoundryToolRegistry()

    tool = registry.get_tool("morningstar")

    # Phase 1: プレースホルダーオブジェクト (dict) を返す
    assert tool is not None
    assert isinstance(tool, dict)
    assert tool["name"] == "morningstar"


def test_get_tool_unknown(mock_env_vars):
    """存在しないツール名でのエラーテスト"""
    registry = FoundryToolRegistry()

    with pytest.raises(ValueError, match="Unsupported tool: unknown_tool"):
        registry.get_tool("unknown_tool")


def test_get_tools_for_agent_melchior(mock_env_vars):
    """Melchior エージェントのツールリスト取得テスト"""
    registry = FoundryToolRegistry()

    tools = registry.get_tools_for_agent("Melchior")

    assert len(tools) == 1
    assert isinstance(tools[0], dict)
    assert tools[0]["name"] == "morningstar"


def test_get_tools_for_agent_unknown(mock_env_vars):
    """未定義エージェント名でのツールリスト取得テスト"""
    registry = FoundryToolRegistry()

    tools = registry.get_tools_for_agent("UnknownAgent")

    # Phase 1: 空リストを返す
    assert tools == []


def test_list_available_tools(mock_env_vars):
    """利用可能なツールリスト取得テスト"""
    registry = FoundryToolRegistry()

    tools = registry.list_available_tools()

    assert "morningstar" in tools
    assert len(tools) == 1  # Phase 1: Morningstar のみ


def test_tool_cache(mock_env_vars):
    """ツールキャッシュの動作テスト"""
    registry = FoundryToolRegistry()

    # 初回取得
    tool1 = registry.get_tool("morningstar")
    assert "morningstar" in registry._tool_cache

    # 2回目取得 (キャッシュから)
    tool2 = registry.get_tool("morningstar")

    # 同じインスタンスが返されることを確認
    assert tool1 is tool2


__all__ = []  # テストモジュールはエクスポート不要
