# TrueNAS Storage Collection for Ansible

Ansible collection for managing TrueNAS storage systems via the middleware REST API.

## Requirements

- Ansible >= 2.15
- TrueNAS CORE 13.0+ or TrueNAS SCALE 22.12+
- API key or admin credentials for TrueNAS

## Installation

```bash
ansible-galaxy collection install truenas.storage
```

Or install from source:

```bash
ansible-galaxy collection install git+https://github.com/sfulmer/ansible-truenas.git
```

## Authentication

All modules require connection parameters. Use an API key (recommended) or username/password:

```yaml
- name: Create a dataset
  truenas.storage.dataset:
    api_url: https://truenas.example.com
    api_key: "{{ truenas_api_key }}"
    name: tank/data
    state: present
```

You can set these as environment variables or group vars to avoid repetition.

## Included Modules

### Storage & ZFS
| Module | Description |
|--------|-------------|
| `truenas.storage.pool` | Manage ZFS pools |
| `truenas.storage.dataset` | Manage ZFS datasets |
| `truenas.storage.snapshot` | Manage ZFS snapshots |
| `truenas.storage.zvol` | Manage ZFS volumes |
| `truenas.storage.replication` | Manage replication tasks |
| `truenas.storage.scrub` | Manage scrub tasks |
| `truenas.storage.smart_test` | Manage S.M.A.R.T. tests |
| `truenas.storage.disk_info` | Get disk information |

### Sharing
| Module | Description |
|--------|-------------|
| `truenas.storage.smb_share` | Manage SMB/CIFS shares |
| `truenas.storage.nfs_share` | Manage NFS exports |
| `truenas.storage.iscsi_target` | Manage iSCSI targets |
| `truenas.storage.iscsi_extent` | Manage iSCSI extents |
| `truenas.storage.iscsi_portal` | Manage iSCSI portals |
| `truenas.storage.webdav_share` | Manage WebDAV shares |

### Networking
| Module | Description |
|--------|-------------|
| `truenas.storage.interface` | Manage network interfaces |
| `truenas.storage.static_route` | Manage static routes |
| `truenas.storage.dns` | Manage DNS configuration |
| `truenas.storage.ipmi` | Manage IPMI configuration |

### Services & System
| Module | Description |
|--------|-------------|
| `truenas.storage.service` | Manage system services |
| `truenas.storage.user` | Manage local users |
| `truenas.storage.group` | Manage local groups |
| `truenas.storage.tunable` | Manage system tunables |
| `truenas.storage.cron` | Manage cron jobs |
| `truenas.storage.mail` | Manage mail configuration |
| `truenas.storage.ntp` | Manage NTP servers |
| `truenas.storage.ups` | Manage UPS configuration |
| `truenas.storage.facts` | Gather TrueNAS system facts |

### Directory Services
| Module | Description |
|--------|-------------|
| `truenas.storage.activedirectory` | Manage Active Directory |
| `truenas.storage.ldap` | Manage LDAP configuration |
| `truenas.storage.kerberos_realm` | Manage Kerberos realms |
| `truenas.storage.kerberos_keytab` | Manage Kerberos keytabs |

### Security & Certificates
| Module | Description |
|--------|-------------|
| `truenas.storage.certificate` | Manage SSL certificates |
| `truenas.storage.ca` | Manage certificate authorities |
| `truenas.storage.acme` | Manage ACME certificates |

### Data Protection
| Module | Description |
|--------|-------------|
| `truenas.storage.cloud_sync` | Manage cloud sync tasks |
| `truenas.storage.rsync_task` | Manage rsync tasks |
| `truenas.storage.config_backup` | System config backup/restore |

### Virtualization & Apps
| Module | Description |
|--------|-------------|
| `truenas.storage.jail` | Manage jails (CORE) |
| `truenas.storage.vm` | Manage virtual machines |
| `truenas.storage.app` | Manage applications (SCALE) |
| `truenas.storage.docker_image` | Manage Docker images |

### High Availability
| Module | Description |
|--------|-------------|
| `truenas.storage.failover` | Initiate HA failover |
| `truenas.storage.ha_config` | Manage HA configuration |

### Monitoring
| Module | Description |
|--------|-------------|
| `truenas.storage.alert_policy` | Manage alert policies |
| `truenas.storage.alert_service` | Manage alert services |
| `truenas.storage.alert_info` | Get current alerts |

## License

GPL-3.0-or-later

## Author

Steve Fulmer ([@sfulmer](https://github.com/sfulmer))
