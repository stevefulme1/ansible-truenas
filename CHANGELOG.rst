================================
stevefulme1.truenas Release Notes
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

Initial release of the ``stevefulme1.truenas`` collection.
This changelog contains all changes to the modules and plugins in this collection.

Major Changes
-------------

- Initial release with 71 modules for managing TrueNAS CORE and SCALE systems via the middleware REST API.
- Shared API client (truenas_api.py) supporting API key and username/password authentication.

New Modules
-----------

- stevefulme1.truenas.acme - Manage ACME DNS authenticators
- stevefulme1.truenas.activedirectory - Configure Active Directory
- stevefulme1.truenas.alert_info - Get current system alerts
- stevefulme1.truenas.alert_policy - Manage alert policies
- stevefulme1.truenas.alert_service - Manage alert notification services
- stevefulme1.truenas.app - Manage applications (SCALE)
- stevefulme1.truenas.ca - Manage Certificate Authorities
- stevefulme1.truenas.certificate - Manage TLS certificates
- stevefulme1.truenas.cloud_credential - Manage cloud credentials
- stevefulme1.truenas.cloud_sync - Manage cloud sync tasks
- stevefulme1.truenas.config_backup - System config backup/restore
- stevefulme1.truenas.dataset - Manage ZFS datasets
- stevefulme1.truenas.dataset_inherit - Reset dataset properties to inherited
- stevefulme1.truenas.dataset_mount - Mount/unmount datasets
- stevefulme1.truenas.dataset_permission - Manage dataset permissions and ACLs
- stevefulme1.truenas.dataset_promote - Promote cloned datasets
- stevefulme1.truenas.dataset_unlock - Unlock encrypted datasets
- stevefulme1.truenas.disk_info - Get disk information
- stevefulme1.truenas.dns - Manage DNS configuration
- stevefulme1.truenas.docker_image - Manage Docker images
- stevefulme1.truenas.facts - Gather TrueNAS system facts
- stevefulme1.truenas.failover - Initiate HA failover
- stevefulme1.truenas.group - Manage local groups
- stevefulme1.truenas.ha_config - Manage HA configuration
- stevefulme1.truenas.init_script - Manage init/shutdown scripts
- stevefulme1.truenas.interface - Manage network interfaces
- stevefulme1.truenas.iscsi_extent - Manage iSCSI extents
- stevefulme1.truenas.iscsi_initiator - Manage iSCSI initiators
- stevefulme1.truenas.iscsi_portal - Manage iSCSI portals
- stevefulme1.truenas.iscsi_target - Manage iSCSI targets
- stevefulme1.truenas.iscsi_targetextent - Manage iSCSI target-extent associations
- stevefulme1.truenas.kerberos_keytab - Manage Kerberos keytabs
- stevefulme1.truenas.kerberos_realm - Manage Kerberos realms
- stevefulme1.truenas.lag - Manage link aggregation (LAGG)
- stevefulme1.truenas.ldap - Configure LDAP directory service
- stevefulme1.truenas.mail - Manage mail/SMTP configuration
- stevefulme1.truenas.nfs_config - Configure global NFS settings
- stevefulme1.truenas.nfs_kerberos - Configure NFS Kerberos settings
- stevefulme1.truenas.nfs_share - Manage NFS exports
- stevefulme1.truenas.ntp - Manage NTP servers
- stevefulme1.truenas.pool - Manage ZFS storage pools
- stevefulme1.truenas.pool_export - Export/disconnect a ZFS pool
- stevefulme1.truenas.pool_resilver - Configure pool resilver priority
- stevefulme1.truenas.pool_scrub - Configure pool scrub schedules
- stevefulme1.truenas.pool_upgrade - Upgrade ZFS pool feature flags
- stevefulme1.truenas.privilege - Manage user privileges
- stevefulme1.truenas.replication - Manage replication tasks
- stevefulme1.truenas.replication_restore - Restore from a replication
- stevefulme1.truenas.replication_run - Trigger a replication run
- stevefulme1.truenas.reporting - Configure reporting/graphing settings
- stevefulme1.truenas.rsync_task - Manage rsync tasks
- stevefulme1.truenas.service - Manage system services
- stevefulme1.truenas.shell_info - Get available user shells
- stevefulme1.truenas.smb_acl - Manage SMB share ACLs
- stevefulme1.truenas.smb_config - Configure global SMB settings
- stevefulme1.truenas.smb_share - Manage SMB/CIFS shares
- stevefulme1.truenas.smb_status_info - Get SMB service status
- stevefulme1.truenas.snapshot - Manage ZFS snapshots
- stevefulme1.truenas.snapshot_clone - Clone a ZFS snapshot
- stevefulme1.truenas.snapshot_rollback - Rollback to a ZFS snapshot
- stevefulme1.truenas.snapshot_task - Manage periodic snapshot tasks
- stevefulme1.truenas.snmp - Configure SNMP service
- stevefulme1.truenas.ssh - Configure SSH service
- stevefulme1.truenas.ssh_connection - Manage SSH connections/keypairs
- stevefulme1.truenas.static_route - Manage static routes
- stevefulme1.truenas.syslog - Configure remote syslog
- stevefulme1.truenas.system - Manage system general settings
- stevefulme1.truenas.tunable - Manage system tunables
- stevefulme1.truenas.user - Manage local users
- stevefulme1.truenas.vlan - Manage VLAN interfaces
- stevefulme1.truenas.vm - Manage virtual machines
