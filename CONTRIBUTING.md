# Contributing

Thank you for your interest in contributing to this Ansible collection!

## How to Contribute

1. **Fork** this repository
2. **Create a branch** for your change (`git checkout -b feature/my-change`)
3. **Make your changes** following the guidelines below
4. **Test your changes** locally
5. **Submit a pull request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/<your-user>/<repo>.git
cd <repo>

# Install development dependencies
pip install ansible-core ansible-lint flake8 pytest

# Run linting
ansible-lint --strict
flake8 plugins/ --max-line-length=120

# Run sanity tests
mkdir -p /tmp/test/ansible_collections/<namespace>/<collection>
rsync -a --exclude='.git' . /tmp/test/ansible_collections/<namespace>/<collection>/
cd /tmp/test/ansible_collections/<namespace>/<collection>
ansible-test sanity --local
```

## Module Guidelines

- Every module must have `DOCUMENTATION`, `EXAMPLES`, and `RETURN` blocks
- Use real vendor SDK or verified API endpoints -- never fabricate endpoints
- Implement proper idempotency with `get_current_state()` / `needs_update()`
- Support `check_mode` with honest reporting
- Add `elements` to all `type: list` parameters
- Add `no_log: true` to sensitive parameters (passwords, tokens, secrets)
- Add `no_log: false` to non-sensitive parameters that contain "key" or "secret" in the name (e.g., `project_key` is not a secret)
- Author field format: `Author Name (@github_handle)`

## Testing Requirements

- **Unit tests**: Required for new modules (`tests/unit/plugins/modules/test_<module>.py`)
- **Integration tests**: Required for CRUD modules (`tests/integration/targets/<module>/tasks/main.yml`)
- Integration tests must include full CRUD lifecycle with idempotency checks
- No `ignore_errors` in test files
- No skipped tests

## Code Style

- PEP 8 compliant (max line length 120 for flake8, 160 for ansible-test)
- No smart/curly quotes in any Python file
- No blank lines within YAML documentation blocks in Python modules
- Use `autopep8 --select=E302,E303,E305` for blank line formatting

## Commit Messages

Use conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `test:` for test additions
- `docs:` for documentation changes
- `chore:` for maintenance tasks

## License

By contributing, you agree that your contributions will be licensed under
the GNU General Public License v3.0 (see [COPYING](COPYING)).
