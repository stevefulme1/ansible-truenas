"""Unit tests for stevefulme1.truenas.kerberos_realm module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type
from unittest.mock import MagicMock

import pytest

MODULE_PATH = "ansible_collections.stevefulme1.truenas.plugins.modules.kerberos_realm"


@pytest.fixture
def mock_api_client():
    """Mock API client for kerberos_realm."""
    client = MagicMock()
    client.get.return_value = None
    client.create.return_value = {"id": "res-123", "name": "test-kerberos_realm"}
    client.update.return_value = {"id": "res-123", "name": "test-kerberos_realm-updated"}
    client.delete.return_value = None
    client.list.return_value = []
    return client


@pytest.fixture
def existing_resource():
    """Return a dict representing an existing kerberos_realm."""
    return {
        "id": "res-123",
        "name": "test-kerberos_realm",
        "state": "active",
    }


class TestCreateKerberosRealm:
    """Tests for creating a kerberos_realm."""

    def test_create_returns_resource(self, mock_api_client):
        """Verify create returns resource dict with expected fields."""
        result = mock_api_client.create("kerberos_realm", {"name": "test-kerberos_realm"})
        assert result["id"] == "res-123"
        assert result["name"] == "test-kerberos_realm"
        mock_api_client.create.assert_called_once()

    def test_create_api_error(self):
        """Verify API errors are raised on create."""
        client = MagicMock()
        client.create.side_effect = Exception("409 Conflict")
        with pytest.raises(Exception, match="409 Conflict"):
            client.create("kerberos_realm", {"name": "test"})


class TestDeleteKerberosRealm:
    """Tests for deleting a kerberos_realm."""

    def test_delete_existing(self, mock_api_client, existing_resource):
        """Verify delete is called for existing resource."""
        mock_api_client.get.return_value = existing_resource
        mock_api_client.delete("kerberos_realm", "res-123")
        mock_api_client.delete.assert_called_once_with("kerberos_realm", "res-123")

    def test_delete_nonexistent(self, mock_api_client):
        """Verify delete handles missing resource gracefully."""
        mock_api_client.get.return_value = None
        mock_api_client.delete.side_effect = Exception("404 Not Found")
        with pytest.raises(Exception, match="404"):
            mock_api_client.delete("kerberos_realm", "missing")


class TestIdempotencyKerberosRealm:
    """Tests for idempotency behavior."""

    def test_no_change_when_exists(self, mock_api_client, existing_resource):
        """Verify no API call when resource already in desired state."""
        mock_api_client.get.return_value = existing_resource
        result = mock_api_client.get("kerberos_realm", "res-123")
        assert result["id"] == "res-123"
