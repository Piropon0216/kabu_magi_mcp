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
@pytest.fixture(autouse=True, scope="function")
def filter_and_set_foundry_env_vars(monkeypatch):
    """
    各テスト関数の直前でFOUNDRY_で始まる環境変数のみをos.environに残し、
    テスト用の値を必ずセットする。
    """
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
