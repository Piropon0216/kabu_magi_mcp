"""
Unit tests for Foundry Tool Registry
"""


import pytest

from src.common.mcp.foundry_tool_registry import FoundryConfig, FoundryToolRegistry


def test_foundry_config_from_env():
    """FoundryConfig が環境変数から正しく読み込まれるかテスト"""
    config = FoundryConfig(_env_file=None)

    assert config.foundry_endpoint == "https://test.foundry.azure.com"
    assert config.foundry_api_key == "test_api_key_12345"
    assert config.foundry_deployment == "gpt-4o-test"
    assert config.foundry_api_version == "2024-12-01"


def test_foundry_tool_registry_initialization():
    """FoundryToolRegistry の初期化テスト"""
    registry = FoundryToolRegistry()

    assert registry.config.foundry_endpoint == "https://test.foundry.azure.com"
    assert registry._tool_cache == {}


def test_get_tool_morningstar_phase1():
    """Phase 1: Morningstar tool 取得テスト (プレースホルダー)"""
    registry = FoundryToolRegistry()

    tool = registry.get_tool("morningstar")

    # Phase 1: プレースホルダーオブジェクトを返す
    assert tool is not None
    assert hasattr(tool, "name")
    assert tool.name == "morningstar"


def test_get_tool_unknown():
    """存在しないツール名でのエラーテスト"""
    registry = FoundryToolRegistry()

    with pytest.raises(ValueError, match="Tool 'unknown_tool' not found"):
        registry.get_tool("unknown_tool")


def test_get_tools_for_agent_melchior():
    """Melchior エージェントのツールリスト取得テスト"""
    registry = FoundryToolRegistry()

    tools = registry.get_tools_for_agent("Melchior")

    assert len(tools) == 1
    assert tools[0].name == "morningstar"


def test_get_tools_for_agent_unknown():
    """未定義エージェント名でのツールリスト取得テスト"""
    registry = FoundryToolRegistry()

    tools = registry.get_tools_for_agent("UnknownAgent")

    # Phase 1: 空リストを返す
    assert tools == []


def test_list_available_tools():
    """利用可能なツールリスト取得テスト"""
    registry = FoundryToolRegistry()

    tools = registry.list_available_tools()

    assert "morningstar" in tools
    assert len(tools) == 1  # Phase 1: Morningstar のみ


def test_tool_cache():
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
