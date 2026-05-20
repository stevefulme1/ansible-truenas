# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this collection, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, please email security concerns to the maintainers directly or use
[GitHub's private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability).

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.x.x   | Pre-release, best-effort |

## Security Best Practices

When using this collection:

- Store credentials in Ansible Vault or an external secrets manager
- Use `no_log: true` on tasks that handle sensitive data
- Review module parameters marked with `no_log` in the documentation
- Run with the minimum required privileges
