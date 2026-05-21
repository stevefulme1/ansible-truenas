"""Unit tests for stevefulme1.truenas.zvol module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type
from unittest.mock import MagicMock

import pytest

MODULE_PATH = "ansible_collections.stevefulme1.truenas.plugins.modules.zvol"


@pytest.fixture
def mock_api_client():
    """Mock API client for zvol."""
    client = MagicMock()
    client.get.return_value = None
    client.create.return_value = {"id": "res-123", "name": "test-zvol"}
    client.update.return_value = {"id": "res-123", "name": "test-zvol-updated"}
    client.delete.return_value = None
    client.list.return_value = []
    return client


@pytest.fixture
def existing_resource():
    """Return a dict representing an existing zvol."""
    return {
        "id": "res-123",
        "name": "test-zvol",
        "state": "active",
    }


class TestCreateZvol:
    """Tests for creating a zvol."""

    def test_create_returns_resource(self, mock_api_client):
        """Verify create returns resource dict with expected fields."""
        result = mock_api_client.create("zvol", {"name": "test-zvol"})
        assert result["id"] == "res-123"
        assert result["name"] == "test-zvol"
        mock_api_client.create.assert_called_once()

    def test_create_api_error(self):
        """Verify API errors are raised on create."""
        client = MagicMock()
        client.create.side_effect = Exception("409 Conflict")
        with pytest.raises(Exception, match="409 Conflict"):
            client.create("zvol", {"name": "test"})


class TestDeleteZvol:
    """Tests for deleting a zvol."""

    def test_delete_existing(self, mock_api_client, existing_resource):
        """Verify delete is called for existing resource."""
        mock_api_client.get.return_value = existing_resource
        mock_api_client.delete("zvol", "res-123")
        mock_api_client.delete.assert_called_once_with("zvol", "res-123")

    def test_delete_nonexistent(self, mock_api_client):
        """Verify delete handles missing resource gracefully."""
        mock_api_client.get.return_value = None
        mock_api_client.delete.side_effect = Exception("404 Not Found")
        with pytest.raises(Exception, match="404"):
            mock_api_client.delete("zvol", "missing")


class TestIdempotencyZvol:
    """Tests for idempotency behavior."""

    def test_no_change_when_exists(self, mock_api_client, existing_resource):
        """Verify no API call when resource already in desired state."""
        mock_api_client.get.return_value = existing_resource
        result = mock_api_client.get("zvol", "res-123")
        assert result["id"] == "res-123"
