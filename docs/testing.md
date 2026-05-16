# Testing the stevefulme1.truenas Collection

This document describes how to run the test suite for the TrueNAS Ansible
collection locally and in CI.

## Prerequisites

- Python 3.12+
- `ansible-core >= 2.16`
- `pytest`, `pytest-cov` (install via `pip install -r test-requirements.txt`)
- For integration tests: a running TrueNAS instance with API access

## Unit Tests

Unit tests mock the `TrueNASClient` and verify module logic without any
network calls.

```bash
# Run with pytest directly
PYTHONPATH=../../.. pytest tests/unit/ -v --tb=short

# Run via nox
nox -s unit

# Run via tox (if configured)
tox -e py312
```

### What is tested

| Test file | Coverage |
|-----------|----------|
| `test_truenas_api.py` | TrueNASClient auth headers, request dispatch, error handling, job_wait |
| `test_pool.py` | Pool create, delete, update, idempotency |
| `test_dataset.py` | Dataset CRUD, property updates, check mode |
| `test_service.py` | Service enable/disable, check mode |
| `test_nfs_share.py` | NFS share CRUD with path/paths, readonly mapping |
| `test_iscsi_target.py` | iSCSI target CRUD, alias updates |

### PYTHONPATH note

When the checkout lives under `ansible_collections/stevefulme1/truenas/`,
set `PYTHONPATH` to the directory *three levels above* so that Python can
resolve `ansible_collections.stevefulme1.truenas.plugins...` imports.

## Integration Tests

Integration tests run against a real TrueNAS appliance. They require two
environment variables:

```bash
export TRUENAS_API_URL="https://truenas.example.com/api/v2.0"
export TRUENAS_API_KEY="1-abc123..."
```

### Running with ansible-test

```bash
# Safe read-only targets (no destructive changes)
ansible-test integration --local -v network_config_info

# Full CRUD targets (requires a pool named "tank")
ansible-test integration --local -v dataset service nfs_share

# Pool tests (requires spare disks - use with caution)
ansible-test integration --local -v pool
```

### Running with Molecule

```bash
cd extensions/molecule/default
TRUENAS_API_URL="https://..." TRUENAS_API_KEY="..." molecule test
```

## TrueNAS API Connection

1. Log in to the TrueNAS web UI.
2. Navigate to **Credentials > API Keys**.
3. Click **Add** and copy the generated key.
4. The API URL is `https://<truenas-host>/api/v2.0`.
5. For self-signed certificates, set `validate_certs: false`.

## CI Workflow

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs:

| Job | Trigger | Description |
|-----|---------|-------------|
| `sanity` | push, PR | ansible-test sanity across Ansible/Python matrix |
| `lint` | push, PR | ansible-lint |
| `unit` | push, PR | pytest unit tests |
| `integration-mock` | push, PR | Read-only integration targets (no TrueNAS needed) |
| `integration-cloud` | workflow_dispatch only | Full integration against a TrueNAS instance |
| `tox` | push, PR | tox test runner |
| `nox` | push, PR | nox lint + security |
| `security` | push, PR | bandit security scan |
| `codeql` | push, PR | CodeQL analysis |

### Cloud integration secrets

For the `integration-cloud` job, configure these repository secrets in the
`truenas` environment:

- `TRUENAS_API_URL` - Full API URL
- `TRUENAS_API_KEY` - API key

## Linting and Import Checks

```bash
# Lint with nox
nox -s lint

# Verify all modules can be compiled
nox -s import_check

# Security scan
nox -s security
```
