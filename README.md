# TrueNAS Storage Collection for Ansible

Ansible collection for managing TrueNAS storage systems via the middleware REST API.

## Requirements

- Ansible >= 2.15
- TrueNAS CORE 13.0+ or TrueNAS SCALE 22.12+
- API key or admin credentials for TrueNAS

## Installation

```bash
ansible-galaxy collection install stevefulme1.storage
```

Or install from source:

```bash
ansible-galaxy collection install git+https://github.com/sfulmer/ansible-truenas.git
```

## Authentication

All modules require connection parameters. Use an API key (recommended) or username/password:

```yaml
- name: Create a dataset
  stevefulme1.storage.dataset:
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
| `stevefulme1.storage.pool` | Manage ZFS pools |
| `stevefulme1.storage.dataset` | Manage ZFS datasets |
| `stevefulme1.storage.snapshot` | Manage ZFS snapshots |
| `stevefulme1.storage.zvol` | Manage ZFS volumes |
| `stevefulme1.storage.replication` | Manage replication tasks |
| `stevefulme1.storage.scrub` | Manage scrub tasks |
| `stevefulme1.storage.smart_test` | Manage S.M.A.R.T. tests |
| `stevefulme1.storage.disk_info` | Get disk information |

### Sharing
| Module | Description |
|--------|-------------|
| `stevefulme1.storage.smb_share` | Manage SMB/CIFS shares |
| `stevefulme1.storage.nfs_share` | Manage NFS exports |
| `stevefulme1.storage.iscsi_target` | Manage iSCSI targets |
| `stevefulme1.storage.iscsi_extent` | Manage iSCSI extents |
| `stevefulme1.storage.iscsi_portal` | Manage iSCSI portals |
| `stevefulme1.storage.webdav_share` | Manage WebDAV shares |

### Networking
| Module | Description |
|--------|-------------|
| `stevefulme1.storage.interface` | Manage network interfaces |
| `stevefulme1.storage.static_route` | Manage static routes |
| `stevefulme1.storage.dns` | Manage DNS configuration |
| `stevefulme1.storage.ipmi` | Manage IPMI configuration |

### Services & System
| Module | Description |
|--------|-------------|
| `stevefulme1.storage.service` | Manage system services |
| `stevefulme1.storage.user` | Manage local users |
| `stevefulme1.storage.group` | Manage local groups |
| `stevefulme1.storage.tunable` | Manage system tunables |
| `stevefulme1.storage.cron` | Manage cron jobs |
| `stevefulme1.storage.mail` | Manage mail configuration |
| `stevefulme1.storage.ntp` | Manage NTP servers |
| `stevefulme1.storage.ups` | Manage UPS configuration |
| `stevefulme1.storage.facts` | Gather TrueNAS system facts |

### Directory Services
| Module | Description |
|--------|-------------|
| `stevefulme1.storage.activedirectory` | Manage Active Directory |
| `stevefulme1.storage.ldap` | Manage LDAP configuration |
| `stevefulme1.storage.kerberos_realm` | Manage Kerberos realms |
| `stevefulme1.storage.kerberos_keytab` | Manage Kerberos keytabs |

### Security & Certificates
| Module | Description |
|--------|-------------|
| `stevefulme1.storage.certificate` | Manage SSL certificates |
| `stevefulme1.storage.ca` | Manage certificate authorities |
| `stevefulme1.storage.acme` | Manage ACME certificates |

### Data Protection
| Module | Description |
|--------|-------------|
| `stevefulme1.storage.cloud_sync` | Manage cloud sync tasks |
| `stevefulme1.storage.rsync_task` | Manage rsync tasks |
| `stevefulme1.storage.config_backup` | System config backup/restore |

### Virtualization & Apps
| Module | Description |
|--------|-------------|
| `stevefulme1.storage.jail` | Manage jails (CORE) |
| `stevefulme1.storage.vm` | Manage virtual machines |
| `stevefulme1.storage.app` | Manage applications (SCALE) |
| `stevefulme1.storage.docker_image` | Manage Docker images |

### High Availability
| Module | Description |
|--------|-------------|
| `stevefulme1.storage.failover` | Initiate HA failover |
| `stevefulme1.storage.ha_config` | Manage HA configuration |

### Monitoring
| Module | Description |
|--------|-------------|
| `stevefulme1.storage.alert_policy` | Manage alert policies |
| `stevefulme1.storage.alert_service` | Manage alert services |
| `stevefulme1.storage.alert_info` | Get current alerts |

## License

GPL-3.0-or-later

## Author

Steve Fulmer ([@sfulmer](https://github.com/sfulmer))
