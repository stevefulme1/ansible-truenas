"""Unit tests for stevefulme1.truenas.nfs_share module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest

MODULE_PATH = "ansible_collections.stevefulme1.truenas.plugins.modules.nfs_share"


def _base_args(**kwargs):
    """Return module args with connection defaults merged."""
    args = {
        "api_url": "https://truenas.local/api/v2.0",
        "api_key": "test-key",
        "username": None,
        "password": None,
        "validate_certs": False,
        "api_timeout": 30,
        "path": "/mnt/tank/data",
        "paths": None,
        "comment": None,
        "networks": None,
        "hosts": None,
        "maproot_user": None,
        "maproot_group": None,
        "mapall_user": None,
        "mapall_group": None,
        "security": None,
        "readonly": False,
        "enabled": True,
        "state": "present",
    }
    args.update(kwargs)
    return args


def _run_module(args, client, check_mode=False):
    from ansible_collections.stevefulme1.truenas.plugins.modules.nfs_share import main

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
    """Test NFS share creation."""

    def test_create_nfs_share(self):
        client = MagicMock()
        client.get.return_value = []
        client.post.return_value = {"id": 1, "path": "/mnt/tank/data", "enabled": True}

        mod = _run_module(
            _base_args(path="/mnt/tank/data", networks=["10.0.0.0/24"]), client
        )

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.post.assert_called_once()
        post_payload = client.post.call_args[0][1]
        assert post_payload["path"] == "/mnt/tank/data"
        assert post_payload["networks"] == ["10.0.0.0/24"]

    def test_create_with_readonly(self):
        client = MagicMock()
        client.get.return_value = []
        client.post.return_value = {"id": 2, "path": "/mnt/tank/media", "ro": True}

        mod = _run_module(
            _base_args(path="/mnt/tank/media", readonly=True), client
        )

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        post_payload = client.post.call_args[0][1]
        # readonly maps to 'ro' in API via _field_map
        assert post_payload["ro"] is True

    def test_create_with_paths_list(self):
        """Test creation with TrueNAS 25.04+ paths list."""
        client = MagicMock()
        client.get.return_value = []
        client.post.return_value = {"id": 3, "paths": ["/mnt/tank/a", "/mnt/tank/b"]}

        mod = _run_module(
            _base_args(path=None, paths=["/mnt/tank/a", "/mnt/tank/b"]), client
        )

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True

    def test_create_check_mode(self):
        client = MagicMock()
        client.get.return_value = []

        mod = _run_module(_base_args(), client, check_mode=True)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.post.assert_not_called()


class TestDelete:
    """Test NFS share deletion."""

    def test_delete_existing_share(self):
        client = MagicMock()
        client.get.return_value = [
            {"id": 1, "path": "/mnt/tank/data", "enabled": True}
        ]

        mod = _run_module(_base_args(state="absent"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.delete.assert_called_once_with("sharing/nfs/id/1")

    def test_delete_nonexistent(self):
        client = MagicMock()
        client.get.return_value = []

        mod = _run_module(_base_args(state="absent"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is False


class TestUpdate:
    """Test NFS share property updates."""

    def test_update_networks(self):
        client = MagicMock()
        client.get.return_value = [
            {"id": 1, "path": "/mnt/tank/data", "networks": ["10.0.0.0/24"],
             "enabled": True, "ro": False}
        ]
        client.put.return_value = {"id": 1, "networks": ["192.168.1.0/24"]}

        mod = _run_module(
            _base_args(networks=["192.168.1.0/24"]), client
        )

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.put.assert_called_once()

    def test_update_maproot_user(self):
        client = MagicMock()
        client.get.return_value = [
            {"id": 1, "path": "/mnt/tank/data", "maproot_user": "",
             "enabled": True, "ro": False}
        ]
        client.put.return_value = {"id": 1, "maproot_user": "root"}

        mod = _run_module(_base_args(maproot_user="root"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True


class TestIdempotent:
    """Test no changes when config matches."""

    def test_no_change_when_identical(self):
        client = MagicMock()
        client.get.return_value = [
            {"id": 1, "path": "/mnt/tank/data", "ro": False, "enabled": True}
        ]

        mod = _run_module(_base_args(), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is False
        client.put.assert_not_called()
        client.post.assert_not_called()
