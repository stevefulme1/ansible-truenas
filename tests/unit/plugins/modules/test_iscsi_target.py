"""Unit tests for stevefulme1.truenas.iscsi_target module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest

MODULE_PATH = "ansible_collections.stevefulme1.truenas.plugins.modules.iscsi_target"


def _base_args(**kwargs):
    """Return module args with connection defaults merged."""
    args = {
        "api_url": "https://truenas.local/api/v2.0",
        "api_key": "test-key",
        "username": None,
        "password": None,
        "validate_certs": False,
        "api_timeout": 30,
        "name": "iqn.2024-01.com.example:storage",
        "alias": None,
        "groups": None,
        "state": "present",
    }
    args.update(kwargs)
    return args


def _run_module(args, client, check_mode=False):
    from ansible_collections.stevefulme1.truenas.plugins.modules.iscsi_target import main

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
    """Test iSCSI target creation."""

    def test_create_target(self):
        client = MagicMock()
        client.get.return_value = []
        client.post.return_value = {"id": 1, "name": "iqn.2024-01.com.example:storage"}

        mod = _run_module(_base_args(alias="Main Storage"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.post.assert_called_once()
        post_payload = client.post.call_args[0][1]
        assert post_payload["name"] == "iqn.2024-01.com.example:storage"
        assert post_payload["alias"] == "Main Storage"

    def test_create_with_groups(self):
        client = MagicMock()
        client.get.return_value = []
        client.post.return_value = {
            "id": 2, "name": "iqn.2024-01.com.example:backup",
            "groups": [{"portal": 1, "initiator": 1}],
        }

        mod = _run_module(
            _base_args(
                name="iqn.2024-01.com.example:backup",
                groups=[{"portal": 1, "initiator": 1}],
            ),
            client,
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
    """Test iSCSI target deletion."""

    def test_delete_existing_target(self):
        client = MagicMock()
        client.get.return_value = [
            {"id": 1, "name": "iqn.2024-01.com.example:storage"}
        ]

        mod = _run_module(_base_args(state="absent"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.delete.assert_called_once_with("iscsi/target/id/1")

    def test_delete_nonexistent(self):
        client = MagicMock()
        client.get.return_value = []

        mod = _run_module(_base_args(state="absent"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is False


class TestUpdate:
    """Test iSCSI target property updates."""

    def test_update_alias(self):
        client = MagicMock()
        client.get.return_value = [
            {"id": 1, "name": "iqn.2024-01.com.example:storage", "alias": "Old Name"}
        ]
        client.put.return_value = {
            "id": 1, "name": "iqn.2024-01.com.example:storage", "alias": "New Name"
        }

        mod = _run_module(_base_args(alias="New Name"), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.put.assert_called_once()
        put_payload = client.put.call_args[0][1]
        assert put_payload["alias"] == "New Name"


class TestIdempotent:
    """Test no changes when config matches."""

    def test_no_change_when_identical(self):
        client = MagicMock()
        client.get.return_value = [
            {"id": 1, "name": "iqn.2024-01.com.example:storage"}
        ]

        mod = _run_module(_base_args(), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is False
        client.put.assert_not_called()
        client.post.assert_not_called()
