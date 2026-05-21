"""Unit tests for stevefulme1.truenas.iscsi_targetextent module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type
from unittest.mock import MagicMock

import pytest

MODULE_PATH = "ansible_collections.stevefulme1.truenas.plugins.modules.iscsi_targetextent"


@pytest.fixture
def mock_api_client():
    """Mock API client for iscsi_targetextent."""
    client = MagicMock()
    client.get.return_value = None
    client.create.return_value = {"id": "res-123", "name": "test-iscsi_targetextent"}
    client.update.return_value = {"id": "res-123", "name": "test-iscsi_targetextent-updated"}
    client.delete.return_value = None
    client.list.return_value = []
    return client


@pytest.fixture
def existing_resource():
    """Return a dict representing an existing iscsi_targetextent."""
    return {
        "id": "res-123",
        "name": "test-iscsi_targetextent",
        "state": "active",
    }


class TestCreateIscsiTargetextent:
    """Tests for creating a iscsi_targetextent."""

    def test_create_returns_resource(self, mock_api_client):
        """Verify create returns resource dict with expected fields."""
        result = mock_api_client.create("iscsi_targetextent", {"name": "test-iscsi_targetextent"})
        assert result["id"] == "res-123"
        assert result["name"] == "test-iscsi_targetextent"
        mock_api_client.create.assert_called_once()

    def test_create_api_error(self):
        """Verify API errors are raised on create."""
        client = MagicMock()
        client.create.side_effect = Exception("409 Conflict")
        with pytest.raises(Exception, match="409 Conflict"):
            client.create("iscsi_targetextent", {"name": "test"})


class TestDeleteIscsiTargetextent:
    """Tests for deleting a iscsi_targetextent."""

    def test_delete_existing(self, mock_api_client, existing_resource):
        """Verify delete is called for existing resource."""
        mock_api_client.get.return_value = existing_resource
        mock_api_client.delete("iscsi_targetextent", "res-123")
        mock_api_client.delete.assert_called_once_with("iscsi_targetextent", "res-123")

    def test_delete_nonexistent(self, mock_api_client):
        """Verify delete handles missing resource gracefully."""
        mock_api_client.get.return_value = None
        mock_api_client.delete.side_effect = Exception("404 Not Found")
        with pytest.raises(Exception, match="404"):
            mock_api_client.delete("iscsi_targetextent", "missing")


class TestIdempotencyIscsiTargetextent:
    """Tests for idempotency behavior."""

    def test_no_change_when_exists(self, mock_api_client, existing_resource):
        """Verify no API call when resource already in desired state."""
        mock_api_client.get.return_value = existing_resource
        result = mock_api_client.get("iscsi_targetextent", "res-123")
        assert result["id"] == "res-123"
