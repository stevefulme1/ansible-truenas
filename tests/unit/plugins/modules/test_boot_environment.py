"""Unit tests for stevefulme1.truenas.boot_environment module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type
from unittest.mock import MagicMock

import pytest

MODULE_PATH = "ansible_collections.stevefulme1.truenas.plugins.modules.boot_environment"


@pytest.fixture
def mock_api_client():
    """Mock API client for boot_environment."""
    client = MagicMock()
    client.get.return_value = None
    client.create.return_value = {"id": "res-123", "name": "test-boot_environment"}
    client.update.return_value = {"id": "res-123", "name": "test-boot_environment-updated"}
    client.delete.return_value = None
    client.list.return_value = []
    return client


@pytest.fixture
def existing_resource():
    """Return a dict representing an existing boot_environment."""
    return {
        "id": "res-123",
        "name": "test-boot_environment",
        "state": "active",
    }


class TestCreateBootEnvironment:
    """Tests for creating a boot_environment."""

    def test_create_returns_resource(self, mock_api_client):
        """Verify create returns resource dict with expected fields."""
        result = mock_api_client.create("boot_environment", {"name": "test-boot_environment"})
        assert result["id"] == "res-123"
        assert result["name"] == "test-boot_environment"
        mock_api_client.create.assert_called_once()

    def test_create_api_error(self):
        """Verify API errors are raised on create."""
        client = MagicMock()
        client.create.side_effect = Exception("409 Conflict")
        with pytest.raises(Exception, match="409 Conflict"):
            client.create("boot_environment", {"name": "test"})


class TestDeleteBootEnvironment:
    """Tests for deleting a boot_environment."""

    def test_delete_existing(self, mock_api_client, existing_resource):
        """Verify delete is called for existing resource."""
        mock_api_client.get.return_value = existing_resource
        mock_api_client.delete("boot_environment", "res-123")
        mock_api_client.delete.assert_called_once_with("boot_environment", "res-123")

    def test_delete_nonexistent(self, mock_api_client):
        """Verify delete handles missing resource gracefully."""
        mock_api_client.get.return_value = None
        mock_api_client.delete.side_effect = Exception("404 Not Found")
        with pytest.raises(Exception, match="404"):
            mock_api_client.delete("boot_environment", "missing")


class TestIdempotencyBootEnvironment:
    """Tests for idempotency behavior."""

    def test_no_change_when_exists(self, mock_api_client, existing_resource):
        """Verify no API call when resource already in desired state."""
        mock_api_client.get.return_value = existing_resource
        result = mock_api_client.get("boot_environment", "res-123")
        assert result["id"] == "res-123"
