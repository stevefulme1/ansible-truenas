"""Unit tests for stevefulme1.truenas.dataset module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest

MODULE_PATH = "ansible_collections.stevefulme1.truenas.plugins.modules.dataset"


def _base_args(**kwargs):
    """Return module args with connection defaults merged."""
    args = {
        "api_url": "https://truenas.local/api/v2.0",
        "api_key": "test-key",
        "username": None,
        "password": None,
        "validate_certs": False,
        "api_timeout": 30,
        "name": "tank/data",
        "type": "FILESYSTEM",
        "quota": None,
        "refquota": None,
        "reservation": None,
        "compression": "LZ4",
        "recordsize": None,
        "atime": None,
        "sync": None,
        "copies": None,
        "deduplication": None,
        "encryption": None,
        "volsize": None,
        "volblocksize": None,
        "comments": None,
        "state": "present",
    }
    args.update(kwargs)
    return args


def _run_module(args, client, check_mode=False):
    from ansible_collections.stevefulme1.truenas.plugins.modules.dataset import main

    mod = MagicMock()
    mod.params = args
    mod.check_mode = check_mode
    mod.exit_json = MagicMock(side_effect=SystemExit(0))
    mod.fail_json = MagicMock(side_effect=SystemExit(1))
    with patch(f"{MODULE_PATH}.TrueNASClient", return_value=client), \
         patch(f"{MODULE_PATH}.AnsibleModule", return_value=mod):
        with pytest.raises(SystemExit):
            main()
    return mod


class TestCreate:
    """Test dataset creation."""

    def test_create_dataset(self):
        client = MagicMock()
        client.get.return_value = []
        client.post.return_value = {"id": "tank/data", "name": "tank/data"}

        mod = _run_module(_base_args(quota="100G", compression="LZ4"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.post.assert_called_once()
        post_payload = client.post.call_args[0][1]
        assert post_payload["name"] == "tank/data"
        assert post_payload["quota"] == "100G"

    def test_create_zvol(self):
        client = MagicMock()
        client.get.return_value = []
        client.post.return_value = {"id": "tank/vol1", "name": "tank/vol1"}

        mod = _run_module(
            _base_args(name="tank/vol1", type="VOLUME", volsize="50G", volblocksize="16K"),
            client,
        )

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        post_payload = client.post.call_args[0][1]
        assert post_payload["type"] == "VOLUME"
        assert post_payload["volsize"] == "50G"

    def test_create_check_mode(self):
        client = MagicMock()
        client.get.return_value = []

        mod = _run_module(_base_args(), client, check_mode=True)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.post.assert_not_called()


class TestDelete:
    """Test dataset deletion."""

    def test_delete_existing_dataset(self):
        client = MagicMock()
        client.get.return_value = [
            {"id": "tank/data", "name": "tank/data", "compression": "LZ4"}
        ]

        mod = _run_module(_base_args(state="absent"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.delete.assert_called_once_with("pool/dataset/id/tank/data")

    def test_delete_nonexistent(self):
        client = MagicMock()
        client.get.return_value = []

        mod = _run_module(_base_args(state="absent"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is False
        client.delete.assert_not_called()


class TestUpdate:
    """Test dataset property updates."""

    def test_update_compression(self):
        client = MagicMock()
        client.get.return_value = [
            {"id": "tank/data", "name": "tank/data", "compression": "LZ4",
             "type": "FILESYSTEM"}
        ]
        client.put.return_value = {
            "id": "tank/data", "name": "tank/data", "compression": "ZSTD"
        }

        mod = _run_module(_base_args(compression="ZSTD"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        put_args = client.put.call_args
        assert "compression" in put_args[0][1]

    def test_update_quota(self):
        client = MagicMock()
        client.get.return_value = [
            {"id": "tank/data", "name": "tank/data", "compression": "LZ4",
             "type": "FILESYSTEM", "quota": "50G"}
        ]
        client.put.return_value = {"id": "tank/data", "quota": "200G"}

        mod = _run_module(_base_args(quota="200G"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True

    def test_add_comments(self):
        client = MagicMock()
        client.get.return_value = [
            {"id": "tank/data", "name": "tank/data", "compression": "LZ4",
             "type": "FILESYSTEM"}
        ]
        client.put.return_value = {"id": "tank/data", "comments": "test comment"}

        mod = _run_module(_base_args(comments="test comment"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True


class TestIdempotent:
    """Test that no changes are reported when config matches."""

    def test_no_change_when_identical(self):
        client = MagicMock()
        client.get.return_value = [
            {"id": "tank/data", "name": "tank/data", "type": "FILESYSTEM",
             "compression": "LZ4"}
        ]

        mod = _run_module(_base_args(), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is False
        client.put.assert_not_called()
        client.post.assert_not_called()
