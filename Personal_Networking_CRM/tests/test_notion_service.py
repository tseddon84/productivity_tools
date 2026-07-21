import pytest
from datetime import datetime
from src.notion_service import NotionService

@pytest.fixture
def mock_notion_service(mocker):
    # Mock out the Notion Client so it doesn't hit the real API
    mocker.patch("src.notion_service.Client")
    mocker.patch("src.notion_service.Config.NOTION_TOKEN", "fake")
    return NotionService()

def test_calculate_delta(mock_notion_service):
    """Test that date math correctly returns the day delta."""
    last_contacted = "2026-07-01"
    current_date = datetime(2026, 7, 21) # 20 days later
    
    delta = mock_notion_service.calculate_delta(last_contacted, current_date)
    assert delta == 20

def test_overdue_logic(mock_notion_service, mocker):
    """Test that the engine properly identifies overdue contacts."""
    
    # Mock the Notification Engine so it doesn't send real emails during testing
    mock_dispatch = mocker.patch("src.notion_service.NotificationEngine.dispatch_payload")
    
    # Mock a fake Notion DB payload
    fake_results = [
        {
            "id": "123",
            "properties": {
                "Name": {"title": [{"text": {"content": "John Doe"}}]},
                "Tier": {"select": {"name": "Inner Circle"}}, # 30 day limit
                "Last_Contacted_Date": {"date": {"start": "2026-06-01"}}, # Over 30 days ago
                "Rich_Text_Notes": {"rich_text": [{"text": {"content": "Note"}}]},
                "I_Contacted_Them_Today": {"checkbox": False}
            }
        },
        {
            "id": "456",
            "properties": {
                "Name": {"title": [{"text": {"content": "Jane Smith"}}]},
                "Tier": {"select": {"name": "Mentor"}}, # 90 day limit
                "Last_Contacted_Date": {"date": {"start": "2026-07-01"}}, # Under 90 days ago
                "Rich_Text_Notes": {"rich_text": [{"text": {"content": "Note"}}]},
                "I_Contacted_Them_Today": {"checkbox": False}
            }
        }
    ]
    
    # Inject the fake payload into the mocked Notion client
    mock_notion_service.notion.databases.query.return_value.get.return_value = fake_results
    
    # Run the engine as if today is July 21, 2026
    fake_today = datetime(2026, 7, 21)
    mock_notion_service.process_database(current_date=fake_today)
    
    # John Doe (Inner circle, 50 days ago) should trigger the dispatch. Jane Smith (20 days ago) should not.
    mock_dispatch.assert_called_once()
    payload_sent = mock_dispatch.call_args[0][0]
    
    assert "John Doe" in payload_sent
    assert "Jane Smith" not in payload_sent
