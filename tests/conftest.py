import os

import pytest


@pytest.fixture(autouse=True, scope="function")
def filter_and_set_foundry_env_vars(monkeypatch):
    """
    各テスト関数の直前で FOUNDRY_ で始まる環境変数のみを残し、
    テスト用の値をセットする。

    実装は `monkeypatch` を使って環境を隔離するため、後片付けは不要です。
    """
    # If FOUNDRY_PRESERVE_ENV is set to '1', do not override real FOUNDRY_*
    # environment variables. This allows running live integration tests
    # against real services without the test mocks being injected.
    if os.environ.get("FOUNDRY_PRESERVE_ENV") == "1":
        # preserve the real environment for live integration runs
        yield
        return

    # Remove all environment variables that don't start with FOUNDRY_
    # to ensure test isolation. monkeypatch will restore them after the test.
    keys_to_remove = [k for k in os.environ if not k.startswith("FOUNDRY_")]
    for k in keys_to_remove:
        monkeypatch.delenv(k, raising=False)

    # Set required FOUNDRY_ variables for tests.
    monkeypatch.setenv("FOUNDRY_ENDPOINT", "https://test.foundry.azure.com")
    monkeypatch.setenv("FOUNDRY_API_KEY", "test_api_key_12345")
    monkeypatch.setenv("FOUNDRY_DEPLOYMENT", "gpt-4o-test")
    monkeypatch.setenv("FOUNDRY_API_VERSION", "2024-12-01")
    yield
