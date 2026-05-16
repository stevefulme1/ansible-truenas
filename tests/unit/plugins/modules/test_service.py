"""Unit tests for stevefulme1.truenas.service module."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest

MODULE_PATH = "ansible_collections.stevefulme1.truenas.plugins.modules.service"


def _base_args(**kwargs):
    """Return module args with connection defaults merged."""
    args = {
        "api_url": "https://truenas.local/api/v2.0",
        "api_key": "test-key",
        "username": None,
        "password": None,
        "validate_certs": False,
        "api_timeout": 30,
        "service": "ssh",
        "enabled": True,
        "started": True,
    }
    args.update(kwargs)
    return args


def _run_module(args, client, check_mode=False):
    from ansible_collections.stevefulme1.truenas.plugins.modules.service import main

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
    """Test enabling and starting a service."""

    def test_enable_and_start_ssh(self):
        client = MagicMock()
        client.post.return_value = {"service": "ssh", "enabled": True, "started": True}

        mod = _run_module(
            _base_args(service="ssh", enabled=True, started=True), client
        )

        mod.exit_json.assert_called_once()
        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.post.assert_called_once()
        post_payload = client.post.call_args[0][1]
        assert post_payload["service"] == "ssh"
        assert post_payload["enabled"] is True
        assert post_payload["started"] is True

    def test_enable_smb(self):
        client = MagicMock()
        client.post.return_value = {"service": "smb", "enabled": True, "started": True}

        mod = _run_module(
            _base_args(service="smb", enabled=True, started=True), client
        )

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        post_payload = client.post.call_args[0][1]
        assert post_payload["service"] == "smb"


class TestDelete:
    """Test disabling and stopping a service."""

    def test_disable_and_stop_ssh(self):
        client = MagicMock()
        client.post.return_value = {"service": "ssh", "enabled": False, "started": False}

        mod = _run_module(
            _base_args(service="ssh", enabled=False, started=False), client
        )

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        post_payload = client.post.call_args[0][1]
        assert post_payload["enabled"] is False
        assert post_payload["started"] is False


class TestUpdate:
    """Test modifying service state."""

    def test_start_without_enabling(self):
        client = MagicMock()
        client.post.return_value = {"service": "nfs", "enabled": False, "started": True}

        mod = _run_module(
            _base_args(service="nfs", enabled=False, started=True), client
        )

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True


class TestIdempotent:
    """Test check mode skips API calls."""

    def test_check_mode_no_api_call(self):
        client = MagicMock()

        mod = _run_module(_base_args(), client, check_mode=True)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.post.assert_not_called()
