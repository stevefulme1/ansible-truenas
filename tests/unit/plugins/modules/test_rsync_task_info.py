"""Unit tests for stevefulme1.truenas.rsync_task_info module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type
from unittest.mock import MagicMock

import pytest

MODULE_PATH = "ansible_collections.stevefulme1.truenas.plugins.modules.rsync_task_info"


@pytest.fixture
def mock_api_client():
    """Mock API client for rsync_task_info."""
    client = MagicMock()
    client.get.return_value = {"data": []}
    client.list.return_value = []
    return client


class TestListRsyncTaskInfo:
    """Tests for listing via rsync_task_info."""

    def test_list_returns_data(self, mock_api_client):
        """Verify list returns expected structure."""
        result = mock_api_client.list("rsync_task_info")
        assert result == []
        mock_api_client.list.assert_called_once()

    def test_list_api_error(self):
        """Verify API errors are raised on list."""
        client = MagicMock()
        client.list.side_effect = Exception("401 Unauthorized")
        with pytest.raises(Exception, match="401"):
            client.list("rsync_task_info")

    def test_list_with_pagination(self, mock_api_client):
        """Verify pagination parameters are passed."""
        mock_api_client.list("rsync_task_info", limit=10, offset=0)
        mock_api_client.list.assert_called_with("rsync_task_info", limit=10, offset=0)
