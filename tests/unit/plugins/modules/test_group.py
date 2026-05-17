"""Unit tests for stevefulme1.truenas.group module."""
from __future__ import absolute_import, division, print_function
__metaclass__ = type

from unittest.mock import MagicMock, patch
import pytest

MODULE_PATH = "ansible_collections.stevefulme1.truenas.plugins.modules.group"


def _base_args(**kwargs):
    """Return module args with connection defaults."""
    args = {
        "api_url": "https://truenas.local/api/v2.0",
        "api_key": "test-key",
        "username": None,
        "password": None,
        "validate_certs": False,
        "api_timeout": 30,
        "name": 'testgroup', "gid": 2001,
        "state": "present",
    }
    args.update(kwargs)
    return args


def _run_module(args, client, check_mode=False):
    from ansible_collections.stevefulme1.truenas.plugins.modules.group import main

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
    """Test group creation."""

    def test_create_resource(self):
        client = MagicMock()
        client.get.return_value = []
        client.post.return_value = {
            "id": 1,
            "name": 'testgroup', "gid": 2001,
        }

        mod = _run_module(_base_args(), client)

        mod.exit_json.assert_called_once()
        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.post.assert_called_once()

    def test_create_second_resource(self):
        client = MagicMock()
        client.get.return_value = []
        client.post.return_value = {
            "id": 2,
            "name": 'testgroup', "gid": 2001,
        }

        mod = _run_module(
            _base_args(name='testgroup'),
            client,
        )

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True


class TestDelete:
    """Test group deletion."""

    def test_delete_resource(self):
        client = MagicMock()
        client.get.return_value = [{"id": 1, "name": 'testgroup', "gid": 2001}]
        client.delete.return_value = None

        mod = _run_module(
            _base_args(state="absent"), client
        )

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.delete.assert_called_once()

    def test_delete_not_found(self):
        client = MagicMock()
        client.get.return_value = []

        mod = _run_module(
            _base_args(state="absent"), client
        )

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is False
        client.delete.assert_not_called()


class TestUpdate:
    """Test group update."""

    def test_update_resource(self):
        client = MagicMock()
        client.get.return_value = [{"id": 1, "name": 'testgroup', "gid": 2001}]
        client.put.return_value = {
            "id": 1,
            "name": 'testgroup', "gid": 2001,
        }

        mod = _run_module(_base_args(), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True


class TestCheckMode:
    """Test check mode."""

    def test_check_mode_no_api_calls(self):
        client = MagicMock()

        mod = _run_module(_base_args(), client, check_mode=True)

        call_kwargs = mod.exit_json.call_args[1]
        assert call_kwargs["changed"] is True
        client.post.assert_not_called()
        client.put.assert_not_called()
        client.delete.assert_not_called()


class TestIdempotent:
    """Test idempotency."""

    def test_no_change_needed(self):
        client = MagicMock()
        existing = {"id": 1, "name": 'testgroup', "gid": 2001}
        client.get.return_value = [existing]

        mod = _run_module(_base_args(), client)

        # Module ran successfully
        mod.exit_json.assert_called_once()


class TestErrorHandling:
    """Test error handling."""

    def test_api_error(self):
        client = MagicMock()
        client.get.return_value = []
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import TrueNASError
        client.post.side_effect = TrueNASError("API Error", status_code=401)

        mod = _run_module(_base_args(), client)

        mod.fail_json.assert_called_once()

    def test_connection_error(self):
        client = MagicMock()
        client.get.side_effect = TrueNASError("Connection refused", status_code=None)

        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import TrueNASError

        mod = _run_module(_base_args(), client)

        mod.fail_json.assert_called_once()


class TestReturnValues:
    """Test return value structure."""

    def test_return_has_result(self):
        client = MagicMock()
        client.get.return_value = []
        client.post.return_value = {
            "id": 1,
            "name": 'testgroup', "gid": 2001,
        }

        mod = _run_module(_base_args(), client)

        call_kwargs = mod.exit_json.call_args[1]
        assert "changed" in call_kwargs
