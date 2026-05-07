# TrueNAS Storage Collection for Ansible

Ansible collection for managing TrueNAS storage systems via the middleware REST API.

## Requirements

- Ansible >= 2.15
- TrueNAS CORE 13.0+ or TrueNAS SCALE 22.12+
- API key or admin credentials for TrueNAS

## Installation

```bash
ansible-galaxy collection install stevefulme1.truenas
```

Or install from source:

```bash
ansible-galaxy collection install git+https://github.com/sfulmer/ansible-truenas.git
```

## Authentication

All modules require connection parameters. Use an API key (recommended) or username/password:

```yaml
- name: Create a dataset
  stevefulme1.truenas.dataset:
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
| `stevefulme1.truenas.pool` | Manage ZFS pools |
| `stevefulme1.truenas.dataset` | Manage ZFS datasets |
| `stevefulme1.truenas.snapshot` | Manage ZFS snapshots |
| `stevefulme1.truenas.zvol` | Manage ZFS volumes |
| `stevefulme1.truenas.replication` | Manage replication tasks |
| `stevefulme1.truenas.scrub` | Manage scrub tasks |
| `stevefulme1.truenas.smart_test` | Manage S.M.A.R.T. tests |
| `stevefulme1.truenas.disk_info` | Get disk information |

### Sharing
| Module | Description |
|--------|-------------|
| `stevefulme1.truenas.smb_share` | Manage SMB/CIFS shares |
| `stevefulme1.truenas.nfs_share` | Manage NFS exports |
| `stevefulme1.truenas.iscsi_target` | Manage iSCSI targets |
| `stevefulme1.truenas.iscsi_extent` | Manage iSCSI extents |
| `stevefulme1.truenas.iscsi_portal` | Manage iSCSI portals |
| `stevefulme1.truenas.webdav_share` | Manage WebDAV shares |

### Networking
| Module | Description |
|--------|-------------|
| `stevefulme1.truenas.interface` | Manage network interfaces |
| `stevefulme1.truenas.static_route` | Manage static routes |
| `stevefulme1.truenas.dns` | Manage DNS configuration |
| `stevefulme1.truenas.ipmi` | Manage IPMI configuration |

### Services & System
| Module | Description |
|--------|-------------|
| `stevefulme1.truenas.service` | Manage system services |
| `stevefulme1.truenas.user` | Manage local users |
| `stevefulme1.truenas.group` | Manage local groups |
| `stevefulme1.truenas.tunable` | Manage system tunables |
| `stevefulme1.truenas.cron` | Manage cron jobs |
| `stevefulme1.truenas.mail` | Manage mail configuration |
| `stevefulme1.truenas.ntp` | Manage NTP servers |
| `stevefulme1.truenas.ups` | Manage UPS configuration |
| `stevefulme1.truenas.facts` | Gather TrueNAS system facts |

### Directory Services
| Module | Description |
|--------|-------------|
| `stevefulme1.truenas.activedirectory` | Manage Active Directory |
| `stevefulme1.truenas.ldap` | Manage LDAP configuration |
| `stevefulme1.truenas.kerberos_realm` | Manage Kerberos realms |
| `stevefulme1.truenas.kerberos_keytab` | Manage Kerberos keytabs |

### Security & Certificates
| Module | Description |
|--------|-------------|
| `stevefulme1.truenas.certificate` | Manage SSL certificates |
| `stevefulme1.truenas.ca` | Manage certificate authorities |
| `stevefulme1.truenas.acme` | Manage ACME certificates |

### Data Protection
| Module | Description |
|--------|-------------|
| `stevefulme1.truenas.cloud_sync` | Manage cloud sync tasks |
| `stevefulme1.truenas.rsync_task` | Manage rsync tasks |
| `stevefulme1.truenas.config_backup` | System config backup/restore |

### Virtualization & Apps
| Module | Description |
|--------|-------------|
| `stevefulme1.truenas.jail` | Manage jails (CORE) |
| `stevefulme1.truenas.vm` | Manage virtual machines |
| `stevefulme1.truenas.app` | Manage applications (SCALE) |
| `stevefulme1.truenas.docker_image` | Manage Docker images |

### High Availability
| Module | Description |
|--------|-------------|
| `stevefulme1.truenas.failover` | Initiate HA failover |
| `stevefulme1.truenas.ha_config` | Manage HA configuration |

### Monitoring
| Module | Description |
|--------|-------------|
| `stevefulme1.truenas.alert_policy` | Manage alert policies |
| `stevefulme1.truenas.alert_service` | Manage alert services |
| `stevefulme1.truenas.alert_info` | Get current alerts |

## License

GPL-3.0-or-later

## Author

Steve Fulmer ([@sfulmer](https://github.com/sfulmer))
