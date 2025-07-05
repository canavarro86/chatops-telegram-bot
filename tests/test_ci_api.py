import pytest
import requests
from unittest.mock import patch, MagicMock

from bot.services.ci_api import CIAPI

@pytest.fixture
def ci():
    return CIAPI()

@patch("bot.services.ci_api.requests.post")
def test_trigger_build(mock_post, ci):
    mock_resp = MagicMock(status_code=201)
    mock_resp.raise_for_status.return_value = None
    mock_post.return_value = mock_resp

    result = ci.trigger_build("1234")
    assert result["status"] == 201
    mock_post.assert_called_once()

@patch("bot.services.ci_api.requests.get")
def test_get_last_run(mock_get, ci):
    run = {"id": 42, "status": "completed", "conclusion": "success"}
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"workflow_runs": [run]}
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    last = ci.get_last_run("1234")
    assert last["id"] == 42
    mock_get.assert_called_once()
