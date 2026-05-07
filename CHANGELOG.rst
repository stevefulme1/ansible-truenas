================================
truenas.storage Release Notes
================================

.. contents:: Topics

v1.1.0
======

Release Summary
---------------

Community fixes, security hardening, and expanded CI coverage.
Addresses open issues and PRs from the arensb/ansible-truenas project.

Minor Changes
-------------

- ca - Add TrueNAS SCALE 25.10 compatibility with new ``create_type`` values.
- ca - Add ``add_to_trusted_store`` parameter.
- ca - Add field mapping for ``state_value`` to API field ``state``.
- group - Add ``allow_duplicate_gid`` parameter for non-unique GID support.
- group - Add ``users`` parameter to assign members to a group.
- nfs_share - Add TrueNAS 25.04 compatibility for path/paths field changes.
- nfs_share - Map ``readonly`` param to API field ``ro`` for correct behavior.
- nfs_share - Normalize comment field comparison to handle null vs empty string.
- user - Add ``password_disabled``, ``smb``, ``sudo_commands_nopasswd``, ``microsoft_account``, and ``roles`` (RBAC) parameters.
- user - Add ``update_password`` parameter (``always``/``on_create``) for idempotent password management.
- user - Add ``mutually_exclusive`` validation for ``password`` and ``password_disabled``.

Bugfixes
--------

- activedirectory - Fix ``bindpw`` comparison against API response breaking idempotency.
- group - Fix lookup comparing against wrong field name, preventing idempotent updates.
- ldap - Fix ``bindpw`` comparison against API response breaking idempotency.
- mail - Fix ``pass_value`` comparison against API response breaking idempotency.
- snmp - Fix ``v3_password`` and ``v3_privpassphrase`` comparison against API response breaking idempotency.

Security Fixes
--------------

- cloud_credential - Add ``no_log=True`` to ``attributes`` parameter to prevent cloud provider secrets from appearing in logs.
- kerberos_keytab - Add ``no_log=True`` to ``file`` parameter to prevent keytab content from appearing in logs.
- truenas_api - Replace broad ``except Exception`` with specific ``HTTPError``/``URLError`` handlers to prevent masking programming errors.
- truenas_api - Validate job existence in ``job_wait()`` before polling.
- user, ca, certificate, ssh_connection, cloud_credential - Strip sensitive fields from return values in check mode to prevent credential leakage.

v1.0.0
======

Release Summary
---------------

Initial release of the ``truenas.storage`` collection.
This changelog contains all changes to the modules and plugins in this collection.

Major Changes
-------------

- Initial release with 71 modules for managing TrueNAS CORE and SCALE systems via the middleware REST API.
- Shared API client (truenas_api.py) supporting API key and username/password authentication.

New Modules
-----------

- truenas.storage.acme - Manage ACME DNS authenticators
- truenas.storage.activedirectory - Configure Active Directory
- truenas.storage.alert_info - Get current system alerts
- truenas.storage.alert_policy - Manage alert policies
- truenas.storage.alert_service - Manage alert notification services
- truenas.storage.app - Manage applications (SCALE)
- truenas.storage.ca - Manage Certificate Authorities
- truenas.storage.certificate - Manage TLS certificates
- truenas.storage.cloud_credential - Manage cloud credentials
- truenas.storage.cloud_sync - Manage cloud sync tasks
- truenas.storage.config_backup - System config backup/restore
- truenas.storage.dataset - Manage ZFS datasets
- truenas.storage.dataset_inherit - Reset dataset properties to inherited
- truenas.storage.dataset_mount - Mount/unmount datasets
- truenas.storage.dataset_permission - Manage dataset permissions and ACLs
- truenas.storage.dataset_promote - Promote cloned datasets
- truenas.storage.dataset_unlock - Unlock encrypted datasets
- truenas.storage.disk_info - Get disk information
- truenas.storage.dns - Manage DNS configuration
- truenas.storage.docker_image - Manage Docker images
- truenas.storage.facts - Gather TrueNAS system facts
- truenas.storage.failover - Initiate HA failover
- truenas.storage.group - Manage local groups
- truenas.storage.ha_config - Manage HA configuration
- truenas.storage.init_script - Manage init/shutdown scripts
- truenas.storage.interface - Manage network interfaces
- truenas.storage.iscsi_extent - Manage iSCSI extents
- truenas.storage.iscsi_initiator - Manage iSCSI initiators
- truenas.storage.iscsi_portal - Manage iSCSI portals
- truenas.storage.iscsi_target - Manage iSCSI targets
- truenas.storage.iscsi_targetextent - Manage iSCSI target-extent associations
- truenas.storage.kerberos_keytab - Manage Kerberos keytabs
- truenas.storage.kerberos_realm - Manage Kerberos realms
- truenas.storage.lag - Manage link aggregation (LAGG)
- truenas.storage.ldap - Configure LDAP directory service
- truenas.storage.mail - Manage mail/SMTP configuration
- truenas.storage.nfs_config - Configure global NFS settings
- truenas.storage.nfs_kerberos - Configure NFS Kerberos settings
- truenas.storage.nfs_share - Manage NFS exports
- truenas.storage.ntp - Manage NTP servers
- truenas.storage.pool - Manage ZFS storage pools
- truenas.storage.pool_export - Export/disconnect a ZFS pool
- truenas.storage.pool_resilver - Configure pool resilver priority
- truenas.storage.pool_scrub - Configure pool scrub schedules
- truenas.storage.pool_upgrade - Upgrade ZFS pool feature flags
- truenas.storage.privilege - Manage user privileges
- truenas.storage.replication - Manage replication tasks
- truenas.storage.replication_restore - Restore from a replication
- truenas.storage.replication_run - Trigger a replication run
- truenas.storage.reporting - Configure reporting/graphing settings
- truenas.storage.rsync_task - Manage rsync tasks
- truenas.storage.service - Manage system services
- truenas.storage.shell_info - Get available user shells
- truenas.storage.smb_acl - Manage SMB share ACLs
- truenas.storage.smb_config - Configure global SMB settings
- truenas.storage.smb_share - Manage SMB/CIFS shares
- truenas.storage.smb_status_info - Get SMB service status
- truenas.storage.snapshot - Manage ZFS snapshots
- truenas.storage.snapshot_clone - Clone a ZFS snapshot
- truenas.storage.snapshot_rollback - Rollback to a ZFS snapshot
- truenas.storage.snapshot_task - Manage periodic snapshot tasks
- truenas.storage.snmp - Configure SNMP service
- truenas.storage.ssh - Configure SSH service
- truenas.storage.ssh_connection - Manage SSH connections/keypairs
- truenas.storage.static_route - Manage static routes
- truenas.storage.syslog - Configure remote syslog
- truenas.storage.system - Manage system general settings
- truenas.storage.tunable - Manage system tunables
- truenas.storage.user - Manage local users
- truenas.storage.vlan - Manage VLAN interfaces
- truenas.storage.vm - Manage virtual machines
