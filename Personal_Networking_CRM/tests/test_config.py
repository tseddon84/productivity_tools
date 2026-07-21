import pytest
import os
from src.config import Config

def test_config_validation_passes(monkeypatch):
    """Test that validation passes when all required env vars are present."""
    monkeypatch.setenv("NOTION_TOKEN", "fake_token")
    monkeypatch.setenv("NOTION_DATABASE_ID", "fake_db")
    monkeypatch.setenv("USE_DISCORD", "false")
    monkeypatch.setenv("USE_EMAIL", "false")
    
    # Reload the class attributes based on the new env
    Config.NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    Config.NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
    Config.USE_DISCORD = False
    Config.USE_EMAIL = False
    
    # Should not raise ValueError
    Config.validate()

def test_config_validation_fails_missing_token(monkeypatch):
    monkeypatch.setenv("NOTION_TOKEN", "")
    monkeypatch.setenv("NOTION_DATABASE_ID", "fake_db")
    
    Config.NOTION_TOKEN = ""
    Config.NOTION_DATABASE_ID = "fake_db"
    
    with pytest.raises(ValueError, match="NOTION_TOKEN is missing"):
        Config.validate()

def test_config_validation_discord_logic(monkeypatch):
    """Test that if USE_DISCORD is true, the webhook URL must be present."""
    monkeypatch.setenv("NOTION_TOKEN", "fake")
    monkeypatch.setenv("NOTION_DATABASE_ID", "fake")
    Config.NOTION_TOKEN = "fake"
    Config.NOTION_DATABASE_ID = "fake"
    
    Config.USE_DISCORD = True
    Config.DISCORD_WEBHOOK_URL = ""
    
    with pytest.raises(ValueError, match="DISCORD_WEBHOOK_URL is missing"):
        Config.validate()
