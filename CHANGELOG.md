# Changelog

All notable changes to **stevefulme1.truenas** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.2] - 2026-05-18

### Security

- Added `no_log: true` to all `password` and `api_key` role arguments to prevent credential exposure in logs
- Changed EDA webhook default listen address from `0.0.0.0` to `127.0.0.1` to prevent unintended network exposure
- Added payload size limit (1 MB) to EDA webhook event source

## [3.1.1] - 2026-05-18

### Security

- Add `no_log=True` to `community` parameter in `snmp` module
- Filter sensitive keys from return values on update path in `certificate`, `ssh_connection`, and `cloud_credential` modules (matching existing create-path filtering)
- Filter sensitive keys from return values in `snmp`, `ldap`, and `mail` config modules

## [3.0.0] - 2026-05-15

### Added

- Unit tests for 10 modules and integration targets
- Pre-commit and linting configuration
- Limit/offset pagination parameters to all `_info` modules
- Production-ready roles with real module calls
- EXAMPLES blocks to all 78 info modules
- GPL headers and DOCUMENTATION indentation fixes for `_info` modules

### Fixed

- Rename role vars to use role prefix and add missing YAML markers
- Add YAML document start markers to `galaxy.yml` and `runtime.yml`
- Remove trailing blank lines from info modules
- Remove broken test files with pylint errors
- Empty `__init__.py` and remove broken test files
- Add missing newline at end of all module files
- Add missing role README files for Galaxy import
- Resolve Galaxy import validation issues
- Add `---` to `ci.yml` and `changelog.yaml`

## [2.1.0] - 2026-05-15

### Added

- 60 read-only info modules for full TrueNAS API coverage
- 2 EDA source plugins for event-driven automation
- 10 Day-2 operation roles (backup, certificate, dataset, network, pool, replication, service, share, snapshot, user)
- Total: 151 modules, 10 roles, full EDA/inventory coverage

### Fixed

- Bad return value key names
- Missing `no_log` on passphrase parameter

## [2.0.0] - 2026-05-08

### Added

- 12 info modules for datasets, pools, snapshots, shares, services, users, VMs, and boot environments
- Update management, enclosure info, ACL templates, and inventory plugin
- Boot environments, zvols, SMART tests, and API keys modules
- Comprehensive test suite

## [1.2.0] - 2026-05-08

### Added

- 71 modules covering ZFS pools, datasets, snapshots, SMB/NFS/iSCSI sharing, networking, services, certificates, replication, cloud sync, virtualization, high availability, and monitoring
- TrueNAS middleware REST API client
- Dynamic inventory plugin
- Example playbooks for all major service areas
