================================
stevefulme1.storage Release Notes
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

Initial release of the ``stevefulme1.storage`` collection.
This changelog contains all changes to the modules and plugins in this collection.

Major Changes
-------------

- Initial release with 71 modules for managing TrueNAS CORE and SCALE systems via the middleware REST API.
- Shared API client (truenas_api.py) supporting API key and username/password authentication.

New Modules
-----------

- stevefulme1.storage.acme - Manage ACME DNS authenticators
- stevefulme1.storage.activedirectory - Configure Active Directory
- stevefulme1.storage.alert_info - Get current system alerts
- stevefulme1.storage.alert_policy - Manage alert policies
- stevefulme1.storage.alert_service - Manage alert notification services
- stevefulme1.storage.app - Manage applications (SCALE)
- stevefulme1.storage.ca - Manage Certificate Authorities
- stevefulme1.storage.certificate - Manage TLS certificates
- stevefulme1.storage.cloud_credential - Manage cloud credentials
- stevefulme1.storage.cloud_sync - Manage cloud sync tasks
- stevefulme1.storage.config_backup - System config backup/restore
- stevefulme1.storage.dataset - Manage ZFS datasets
- stevefulme1.storage.dataset_inherit - Reset dataset properties to inherited
- stevefulme1.storage.dataset_mount - Mount/unmount datasets
- stevefulme1.storage.dataset_permission - Manage dataset permissions and ACLs
- stevefulme1.storage.dataset_promote - Promote cloned datasets
- stevefulme1.storage.dataset_unlock - Unlock encrypted datasets
- stevefulme1.storage.disk_info - Get disk information
- stevefulme1.storage.dns - Manage DNS configuration
- stevefulme1.storage.docker_image - Manage Docker images
- stevefulme1.storage.facts - Gather TrueNAS system facts
- stevefulme1.storage.failover - Initiate HA failover
- stevefulme1.storage.group - Manage local groups
- stevefulme1.storage.ha_config - Manage HA configuration
- stevefulme1.storage.init_script - Manage init/shutdown scripts
- stevefulme1.storage.interface - Manage network interfaces
- stevefulme1.storage.iscsi_extent - Manage iSCSI extents
- stevefulme1.storage.iscsi_initiator - Manage iSCSI initiators
- stevefulme1.storage.iscsi_portal - Manage iSCSI portals
- stevefulme1.storage.iscsi_target - Manage iSCSI targets
- stevefulme1.storage.iscsi_targetextent - Manage iSCSI target-extent associations
- stevefulme1.storage.kerberos_keytab - Manage Kerberos keytabs
- stevefulme1.storage.kerberos_realm - Manage Kerberos realms
- stevefulme1.storage.lag - Manage link aggregation (LAGG)
- stevefulme1.storage.ldap - Configure LDAP directory service
- stevefulme1.storage.mail - Manage mail/SMTP configuration
- stevefulme1.storage.nfs_config - Configure global NFS settings
- stevefulme1.storage.nfs_kerberos - Configure NFS Kerberos settings
- stevefulme1.storage.nfs_share - Manage NFS exports
- stevefulme1.storage.ntp - Manage NTP servers
- stevefulme1.storage.pool - Manage ZFS storage pools
- stevefulme1.storage.pool_export - Export/disconnect a ZFS pool
- stevefulme1.storage.pool_resilver - Configure pool resilver priority
- stevefulme1.storage.pool_scrub - Configure pool scrub schedules
- stevefulme1.storage.pool_upgrade - Upgrade ZFS pool feature flags
- stevefulme1.storage.privilege - Manage user privileges
- stevefulme1.storage.replication - Manage replication tasks
- stevefulme1.storage.replication_restore - Restore from a replication
- stevefulme1.storage.replication_run - Trigger a replication run
- stevefulme1.storage.reporting - Configure reporting/graphing settings
- stevefulme1.storage.rsync_task - Manage rsync tasks
- stevefulme1.storage.service - Manage system services
- stevefulme1.storage.shell_info - Get available user shells
- stevefulme1.storage.smb_acl - Manage SMB share ACLs
- stevefulme1.storage.smb_config - Configure global SMB settings
- stevefulme1.storage.smb_share - Manage SMB/CIFS shares
- stevefulme1.storage.smb_status_info - Get SMB service status
- stevefulme1.storage.snapshot - Manage ZFS snapshots
- stevefulme1.storage.snapshot_clone - Clone a ZFS snapshot
- stevefulme1.storage.snapshot_rollback - Rollback to a ZFS snapshot
- stevefulme1.storage.snapshot_task - Manage periodic snapshot tasks
- stevefulme1.storage.snmp - Configure SNMP service
- stevefulme1.storage.ssh - Configure SSH service
- stevefulme1.storage.ssh_connection - Manage SSH connections/keypairs
- stevefulme1.storage.static_route - Manage static routes
- stevefulme1.storage.syslog - Configure remote syslog
- stevefulme1.storage.system - Manage system general settings
- stevefulme1.storage.tunable - Manage system tunables
- stevefulme1.storage.user - Manage local users
- stevefulme1.storage.vlan - Manage VLAN interfaces
- stevefulme1.storage.vm - Manage virtual machines
