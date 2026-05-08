"""Shared fixtures for stevefulme1.truenas unit tests."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import sys
import os
import types
from unittest.mock import MagicMock

import pytest


# ---------------------------------------------------------------------------
# Wire up the ansible_collections namespace package so imports like
#   ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api
# resolve to the checkout on disk, even when the repo is checked out as a
# standalone directory (not inside ansible_collections/stevefulme1/truenas/).
# ---------------------------------------------------------------------------
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

# Build a synthetic tree:  <tmpdir>/ansible_collections/stevefulme1/truenas -> _REPO_ROOT
# This approach creates real __path__ entries so that pkgutil.resolve_name
# (used by unittest.mock.patch) can traverse the dotted path correctly.

import tempfile as _tempfile

_SYNTH_ROOT = _tempfile.mkdtemp(prefix="truenas_ns_")
_AC_DIR = os.path.join(_SYNTH_ROOT, "ansible_collections")
_NS_DIR = os.path.join(_AC_DIR, "stevefulme1")

os.makedirs(_NS_DIR, exist_ok=True)

# Symlink stevefulme1/truenas -> the actual repo checkout
_LINK = os.path.join(_NS_DIR, "truenas")
if not os.path.exists(_LINK):
    os.symlink(_REPO_ROOT, _LINK)

# Put the synthetic root first on sys.path
if _SYNTH_ROOT not in sys.path:
    sys.path.insert(0, _SYNTH_ROOT)

# Force-create the namespace package modules so Python recognises the chain
for _fqcn, _dir in [
    ("ansible_collections", _AC_DIR),
    ("ansible_collections.stevefulme1", _NS_DIR),
    ("ansible_collections.stevefulme1.truenas", _REPO_ROOT),
]:
    if _fqcn not in sys.modules:
        _m = types.ModuleType(_fqcn)
        _m.__path__ = [_dir]
        _m.__package__ = _fqcn
        _m.__file__ = None
        sys.modules[_fqcn] = _m
    elif not hasattr(sys.modules[_fqcn], "__path__"):
        sys.modules[_fqcn].__path__ = [_dir]


# ---------------------------------------------------------------------------
# Common connection / authentication arguments used across all modules.
# ---------------------------------------------------------------------------
@pytest.fixture
def module_args():
    """Return baseline module arguments for TrueNAS connection."""
    return {
        "api_url": "https://truenas.local/api/v2.0",
        "api_key": "test-key",
        "username": None,
        "password": None,
        "validate_certs": False,
        "api_timeout": 30,
        "state": "present",
    }


@pytest.fixture
def mock_truenas_client():
    """Factory fixture returning a pre-configured MagicMock TrueNASClient.

    The mock exposes the same public methods as the real client:
    get, post, put, delete, job_wait.
    """

    def _factory(**overrides):
        client = MagicMock()
        client.get.return_value = overrides.get("get_return", [])
        client.post.return_value = overrides.get("post_return", {})
        client.put.return_value = overrides.get("put_return", {})
        client.delete.return_value = overrides.get("delete_return", None)
        client.job_wait.return_value = overrides.get("job_wait_return", {})
        return client

    return _factory


# ---------------------------------------------------------------------------
# Helpers for AnsibleModule mocking
# ---------------------------------------------------------------------------
@pytest.fixture
def mock_module(module_args):
    """Return a MagicMock that behaves like AnsibleModule."""
    mod = MagicMock()
    mod.params = dict(module_args)
    mod.check_mode = False
    mod.fail_json = MagicMock(side_effect=SystemExit(1))
    mod.exit_json = MagicMock(side_effect=SystemExit(0))
    return mod


def set_module_args(args):
    """Prepare module arguments for AnsibleModule instantiation in tests."""
    args_json = json.dumps({"ANSIBLE_MODULE_ARGS": args})
    from ansible.module_utils import basic as _basic

    _basic._ANSIBLE_ARGS = args_json.encode("utf-8")
