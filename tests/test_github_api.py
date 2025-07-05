import pytest
import requests
from unittest.mock import patch, MagicMock

from bot.services.github_api import GitHubAPI

@pytest.fixture
def api():
    return GitHubAPI()

@patch("bot.services.github_api.requests.get")
def test_list_issues(mock_get, api):
    mock_resp = MagicMock()
    mock_resp.json.return_value = [{"number": 1, "title": "Test"}]
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    issues = api.list_issues()
    assert isinstance(issues, list)
    assert issues[0]["number"] == 1
    mock_get.assert_called_once()

@patch("bot.services.github_api.requests.post")
def test_comment_issue(mock_post, api):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"html_url": "http://"}
    mock_resp.raise_for_status.return_value = None
    mock_post.return_value = mock_resp

    result = api.comment_issue(1, "Hello")
    assert result["html_url"] == "http://"
    mock_post.assert_called_once()
