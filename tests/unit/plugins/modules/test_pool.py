"""Unit tests for stevefulme1.truenas.pool module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest

# Patch where TrueNASClient is looked up (the module that imports it),
# not where it is defined.
MODULE_PATH = "ansible_collections.stevefulme1.truenas.plugins.modules.pool"


def _base_args(**kwargs):
    """Return module args with connection defaults merged."""
    args = {
        "api_url": "https://truenas.local/api/v2.0",
        "api_key": "test-key",
        "username": None,
        "password": None,
        "validate_certs": False,
        "api_timeout": 30,
        "name": "tank",
        "topology": None,
        "encryption": False,
        "encryption_algorithm": "AES-256-GCM",
        "deduplication": "OFF",
        "checksum": "ON",
        "state": "present",
    }
    args.update(kwargs)
    return args


def _make_module(args, check_mode=False):
    mod = MagicMock()
    mod.params = args
    mod.check_mode = check_mode
    mod.exit_json = MagicMock(side_effect=SystemExit(0))
    mod.fail_json = MagicMock(side_effect=SystemExit(1))
    return mod


def _run_module(args, mock_client, check_mode=False):
    """Import and run main(), return the mock AnsibleModule."""
    from ansible_collections.stevefulme1.truenas.plugins.modules.pool import main

    mod = _make_module(args, check_mode=check_mode)
    with patch(f"{MODULE_PATH}.TrueNASClient", return_value=mock_client), \
         patch(f"{MODULE_PATH}.AnsibleModule", return_value=mod):
        with pytest.raises(SystemExit):
            main()
    return mod


class TestCreate:
    """Test pool creation."""

    def test_create_pool(self):
        client = MagicMock()
        client.get.return_value = []
        client.post.return_value = {"id": 1, "name": "tank"}

        args = _base_args(
            topology={"data": [{"type": "MIRROR", "disks": ["sda", "sdb"]}]}
        )
        mod = _run_module(args, client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.post.assert_called_once()

    def test_create_pool_check_mode(self):
        client = MagicMock()
        client.get.return_value = []

        mod = _run_module(_base_args(), client, check_mode=True)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.post.assert_not_called()


class TestDelete:
    """Test pool deletion."""

    def test_delete_existing_pool(self):
        client = MagicMock()
        client.get.return_value = [{"id": 1, "name": "tank"}]

        mod = _run_module(_base_args(state="absent"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.delete.assert_called_once_with("pool/id/1")

    def test_delete_nonexistent_pool(self):
        client = MagicMock()
        client.get.return_value = []

        mod = _run_module(_base_args(state="absent"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is False
        client.delete.assert_not_called()


class TestUpdate:
    """Test pool property updates."""

    def test_update_deduplication(self):
        client = MagicMock()
        client.get.return_value = [
            {"id": 1, "name": "tank", "deduplication": "OFF", "checksum": "ON",
             "encryption": False, "encryption_algorithm": "AES-256-GCM"}
        ]
        client.put.return_value = {"id": 1, "name": "tank", "deduplication": "ON"}

        mod = _run_module(_base_args(deduplication="ON"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.put.assert_called_once()


class TestIdempotent:
    """Test that no changes are reported when config matches."""

    def test_no_change_when_identical(self):
        client = MagicMock()
        client.get.return_value = [
            {"id": 1, "name": "tank", "encryption": False,
             "encryption_algorithm": "AES-256-GCM", "deduplication": "OFF",
             "checksum": "ON"}
        ]

        mod = _run_module(_base_args(), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is False
        client.put.assert_not_called()
        client.post.assert_not_called()
