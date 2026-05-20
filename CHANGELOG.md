# Changelog

All notable changes to **stevefulme1.truenas** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-20

### Added

- 73 action modules covering ZFS pools, datasets, snapshots, SMB/NFS/iSCSI sharing,
  networking, services, certificates, replication, cloud sync, virtualization,
  high availability, and monitoring via the TrueNAS middleware REST API
- 78 read-only info modules for full TrueNAS API coverage
- TrueNAS middleware REST API client (`truenas_api` module_utils)
- Shared `truenas` documentation fragment for common auth parameters
- Dynamic inventory plugin
- 11 production-ready roles for storage, networking, sharing, security, and more
- 2 EDA source plugins for event-driven automation
- Example playbooks for all major service areas
- Integration test targets
- Pre-commit and linting configuration

### Fixed

- All info modules now have complete implementations (RETURN, main function)
- Role tasks use correct module parameter names (`api_url` instead of `host`)
- Integration test tasks pass required module arguments
- `no_log: true` on all password and API key parameters
- Sensitive keys filtered from return values in credential modules
