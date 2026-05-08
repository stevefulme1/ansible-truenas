"""Unit tests for TrueNASClient and truenas_argument_spec."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from io import BytesIO
from unittest.mock import MagicMock, patch, call

import pytest

CLIENT_PATH = "ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _make_module(**params):
    """Create a minimal mock AnsibleModule with sensible defaults."""
    defaults = {
        "api_url": "https://truenas.local",
        "api_key": "test-api-key",
        "username": None,
        "password": None,
        "validate_certs": False,
        "api_timeout": 30,
    }
    defaults.update(params)
    mod = MagicMock()
    mod.params = defaults
    mod.fail_json = MagicMock(side_effect=SystemExit(1))
    return mod


def _make_response(body, code=200):
    """Create a mock HTTP response object."""
    resp = MagicMock()
    resp.read.return_value = json.dumps(body).encode("utf-8") if body is not None else b""
    resp.getcode.return_value = code
    return resp


# ---------------------------------------------------------------------------
# Auth header tests
# ---------------------------------------------------------------------------
class TestAuthHeaders:
    """Verify that TrueNASClient generates proper auth headers."""

    def test_api_key_bearer_header(self):
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            TrueNASClient,
        )

        module = _make_module(api_key="my-secret-key")
        client = TrueNASClient(module)
        headers = client._headers()
        assert headers["Authorization"] == "Bearer my-secret-key"
        assert headers["Content-Type"] == "application/json"

    def test_basic_auth_no_bearer(self):
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            TrueNASClient,
        )

        module = _make_module(api_key=None, username="admin", password="secret")
        client = TrueNASClient(module)
        headers = client._headers()
        assert "Authorization" not in headers
        auth = client._auth()
        assert auth == ("admin", "secret")

    def test_no_credentials_fails(self):
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            TrueNASClient,
        )

        module = _make_module(api_key=None, username=None, password=None)
        with pytest.raises(SystemExit):
            TrueNASClient(module)
        module.fail_json.assert_called_once()


# ---------------------------------------------------------------------------
# Request tests
# ---------------------------------------------------------------------------
class TestRequest:
    """Test the request() method dispatches correctly to open_url."""

    @patch(f"{CLIENT_PATH}.open_url")
    def test_get_request(self, mock_open_url):
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            TrueNASClient,
        )

        mock_open_url.return_value = _make_response({"id": 1, "name": "tank"})
        module = _make_module()
        client = TrueNASClient(module)

        result = client.get("pool")

        mock_open_url.assert_called_once()
        assert result == {"id": 1, "name": "tank"}
        args, kwargs = mock_open_url.call_args
        assert "pool" in args[0]
        assert kwargs["method"] == "GET"

    @patch(f"{CLIENT_PATH}.open_url")
    def test_get_with_params(self, mock_open_url):
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            TrueNASClient,
        )

        mock_open_url.return_value = _make_response([{"id": 1}])
        module = _make_module()
        client = TrueNASClient(module)

        client.get("core/get_jobs", params={"id": 42})

        args, _ = mock_open_url.call_args
        assert "id=42" in args[0]

    @patch(f"{CLIENT_PATH}.open_url")
    def test_post_sends_body(self, mock_open_url):
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            TrueNASClient,
        )

        mock_open_url.return_value = _make_response({"id": 5})
        module = _make_module()
        client = TrueNASClient(module)

        result = client.post("pool/dataset", {"name": "tank/test"})

        assert result == {"id": 5}
        _, kwargs = mock_open_url.call_args
        assert kwargs["method"] == "POST"
        body = json.loads(kwargs["data"])
        assert body["name"] == "tank/test"

    @patch(f"{CLIENT_PATH}.open_url")
    def test_put_sends_body(self, mock_open_url):
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            TrueNASClient,
        )

        mock_open_url.return_value = _make_response({"id": 5, "compression": "ZSTD"})
        module = _make_module()
        client = TrueNASClient(module)

        result = client.put("pool/dataset/id/5", {"compression": "ZSTD"})

        _, kwargs = mock_open_url.call_args
        assert kwargs["method"] == "PUT"

    @patch(f"{CLIENT_PATH}.open_url")
    def test_delete_request(self, mock_open_url):
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            TrueNASClient,
        )

        mock_open_url.return_value = _make_response(None)
        module = _make_module()
        client = TrueNASClient(module)

        result = client.delete("pool/dataset/id/5")

        _, kwargs = mock_open_url.call_args
        assert kwargs["method"] == "DELETE"
        assert result is None


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------
class TestErrorHandling:
    """Verify proper exception wrapping for HTTP and URL errors."""

    @patch(f"{CLIENT_PATH}.open_url")
    def test_http_error_raises_truenas_error(self, mock_open_url):
        from ansible.module_utils.six.moves.urllib.error import HTTPError
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            TrueNASClient,
            TrueNASError,
        )

        error_body = json.dumps({"message": "Not found"}).encode("utf-8")
        exc = HTTPError(
            "https://truenas.local/api/v2.0/pool",
            404,
            "Not Found",
            {},
            BytesIO(error_body),
        )
        mock_open_url.side_effect = exc

        module = _make_module()
        client = TrueNASClient(module)

        with pytest.raises(TrueNASError) as exc_info:
            client.get("pool")
        assert exc_info.value.status_code == 404
        assert "Not found" in str(exc_info.value)

    @patch(f"{CLIENT_PATH}.open_url")
    def test_url_error_raises_truenas_error(self, mock_open_url):
        from ansible.module_utils.six.moves.urllib.error import URLError
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            TrueNASClient,
            TrueNASError,
        )

        mock_open_url.side_effect = URLError("Connection refused")

        module = _make_module()
        client = TrueNASClient(module)

        with pytest.raises(TrueNASError) as exc_info:
            client.get("pool")
        assert "Connection refused" in str(exc_info.value)


# ---------------------------------------------------------------------------
# job_wait
# ---------------------------------------------------------------------------
class TestJobWait:
    """Test async job polling."""

    @patch(f"{CLIENT_PATH}.open_url")
    def test_job_wait_success(self, mock_open_url):
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            TrueNASClient,
        )

        # First call: RUNNING, second call: SUCCESS
        mock_open_url.side_effect = [
            _make_response([{"state": "RUNNING", "id": 1}]),
            _make_response([{"state": "SUCCESS", "id": 1, "result": {"pool": "tank"}}]),
        ]

        module = _make_module()
        client = TrueNASClient(module)

        with patch("time.sleep"):
            result = client.job_wait(1, timeout=10)
        assert result == {"pool": "tank"}

    @patch(f"{CLIENT_PATH}.open_url")
    def test_job_wait_failure(self, mock_open_url):
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            TrueNASClient,
            TrueNASError,
        )

        mock_open_url.return_value = _make_response(
            [{"state": "FAILED", "id": 1, "error": "Disk failure"}]
        )

        module = _make_module()
        client = TrueNASClient(module)

        with pytest.raises(TrueNASError) as exc_info:
            client.job_wait(1, timeout=10)
        assert "FAILED" in str(exc_info.value)

    @patch(f"{CLIENT_PATH}.open_url")
    def test_job_wait_timeout(self, mock_open_url):
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            TrueNASClient,
            TrueNASError,
        )

        mock_open_url.return_value = _make_response([{"state": "RUNNING", "id": 1}])

        module = _make_module()
        client = TrueNASClient(module)

        with patch("time.sleep"):
            with pytest.raises(TrueNASError) as exc_info:
                client.job_wait(1, timeout=2)
        assert "timed out" in str(exc_info.value)

    @patch(f"{CLIENT_PATH}.open_url")
    def test_job_wait_not_found(self, mock_open_url):
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            TrueNASClient,
            TrueNASError,
        )

        mock_open_url.return_value = _make_response([])

        module = _make_module()
        client = TrueNASClient(module)

        with pytest.raises(TrueNASError) as exc_info:
            client.job_wait(999, timeout=10)
        assert "not found" in str(exc_info.value)


# ---------------------------------------------------------------------------
# truenas_argument_spec
# ---------------------------------------------------------------------------
class TestArgumentSpec:
    """Verify the shared argument spec contains expected keys."""

    def test_contains_required_keys(self):
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            truenas_argument_spec,
        )

        spec = truenas_argument_spec()
        assert "api_url" in spec
        assert "api_key" in spec
        assert "username" in spec
        assert "password" in spec
        assert "validate_certs" in spec
        assert "api_timeout" in spec

    def test_api_key_is_no_log(self):
        from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
            truenas_argument_spec,
        )

        spec = truenas_argument_spec()
        assert spec["api_key"].get("no_log") is True
        assert spec["password"].get("no_log") is True
