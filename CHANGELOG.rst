================================
stevefulme1.truenas Release Notes
================================

.. contents:: Topics

v0.1.0
======

Release Summary
---------------

Initial pre-release of the TrueNAS collection for Ansible. Provides 151 modules
(73 action + 78 info) for managing TrueNAS CORE and SCALE systems via the
middleware REST API v2.0.

Major Changes
-------------

- 73 action modules for ZFS pools, datasets, snapshots, SMB/NFS/iSCSI sharing,
  networking, services, certificates, replication, cloud sync, virtualization,
  high availability, and monitoring.
- 78 read-only info modules with full implementations.
- TrueNAS middleware REST API client (``truenas_api`` module_utils).
- Shared ``truenas`` documentation fragment for common auth parameters.
- Dynamic inventory plugin.
- 11 production-ready roles.
- 2 EDA source plugins for event-driven automation.

Bugfixes
--------

- All info modules now have complete implementations with RETURN blocks.
- Role tasks use correct module parameter names.
- Integration test tasks pass required module arguments.
