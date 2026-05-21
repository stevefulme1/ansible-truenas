"""Unit tests for stevefulme1.truenas.dataset_promote_info module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type
from unittest.mock import MagicMock

import pytest

MODULE_PATH = "ansible_collections.stevefulme1.truenas.plugins.modules.dataset_promote_info"


@pytest.fixture
def mock_api_client():
    """Mock API client for dataset_promote_info."""
    client = MagicMock()
    client.get.return_value = {"data": []}
    client.list.return_value = []
    return client


class TestListDatasetPromoteInfo:
    """Tests for listing via dataset_promote_info."""

    def test_list_returns_data(self, mock_api_client):
        """Verify list returns expected structure."""
        result = mock_api_client.list("dataset_promote_info")
        assert result == []
        mock_api_client.list.assert_called_once()

    def test_list_api_error(self):
        """Verify API errors are raised on list."""
        client = MagicMock()
        client.list.side_effect = Exception("401 Unauthorized")
        with pytest.raises(Exception, match="401"):
            client.list("dataset_promote_info")

    def test_list_with_pagination(self, mock_api_client):
        """Verify pagination parameters are passed."""
        mock_api_client.list("dataset_promote_info", limit=10, offset=0)
        mock_api_client.list.assert_called_with("dataset_promote_info", limit=10, offset=0)
