#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: nfs_share
short_description: Manage NFS exports
version_added: "1.0.0"
description:
  - Manage NFS exports on a TrueNAS system via the middleware API.
  - This module manages share configuration only, not filesystem permissions.
    Use C(stevefulme1.truenas.dataset_permission) to manage mount point permissions.
  - Supports both legacy (pre-25.04) and modern TrueNAS API formats.
    In TrueNAS 25.04+, the API may use C(paths) (list) instead of C(path) (string).
options:
  path:
    description: Filesystem path to export
    type: str
  paths:
    description: List of paths to export (TrueNAS 25.04+)
    type: list
    elements: str
  comment:
    description: Export description
    type: str
  networks:
    description: Authorized networks (CIDR)
    type: list
    elements: str
  hosts:
    description: Authorized hosts
    type: list
    elements: str
  maproot_user:
    description: Map root to this user
    type: str
  maproot_group:
    description: Map root to this group
    type: str
  mapall_user:
    description: Map all users to this user
    type: str
  mapall_group:
    description: Map all users to this group
    type: str
  security:
    description: Security flavors (SYS, KRB5, KRB5I, KRB5P)
    type: list
    elements: str
  readonly:
    description: Read-only export
    type: bool
    default: false
  enabled:
    description: Enable the export
    type: bool
    default: true
  state:
    description: Desired state of the resource.
    type: str
    choices: [present, absent]
    default: present
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage manage nfs exports
  stevefulme1.truenas.nfs_share:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    state: present
"""

RETURN = r"""
nfs_share:
  description: The manage nfs exports details.
  returned: success
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
    TrueNASClient,
    TrueNASError,
    truenas_argument_spec,
)

# Map module params to API field names
_field_map = {
    'readonly': 'ro',
}


def _find_existing_share(items, module):
    """Find an existing NFS share by path, checking both path and paths fields."""
    desired_path = module.params.get("path")
    desired_paths = module.params.get("paths")

    for item in items:
        # Check legacy single-path field
        if desired_path and item.get("path") == desired_path:
            return item
        # Check modern paths list field (TrueNAS 25.04+)
        if desired_path and desired_path in (item.get("paths") or []):
            return item
        # Check if desired_paths matches
        if desired_paths and set(desired_paths) == set(item.get("paths") or []):
            return item
        if desired_paths and item.get("path") in desired_paths:
            return item
    return None


def _normalize_value(value):
    """Normalize values for comparison, treating None and empty string as equivalent."""
    if value is None:
        return ""
    return value


def main():
    argument_spec = truenas_argument_spec()
    argument_spec.update(
        path=dict(type="str"),
        paths=dict(type="list", elements="str"),
        comment=dict(type="str"),
        networks=dict(type="list", elements="str"),
        hosts=dict(type="list", elements="str"),
        maproot_user=dict(type="str"),
        maproot_group=dict(type="str"),
        mapall_user=dict(type="str"),
        mapall_group=dict(type="str"),
        security=dict(type="list", elements="str"),
        readonly=dict(type="bool", default=False),
        enabled=dict(type="bool", default=True),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    state = module.params["state"]
    result = dict(changed=False)

    try:
        existing = None
        items = client.get("sharing/nfs")
        if isinstance(items, list):
            existing = _find_existing_share(items, module)

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("sharing/nfs/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            _fields = [
                'path', 'paths', 'comment', 'networks', 'hosts',
                'maproot_user', 'maproot_group', 'mapall_user',
                'mapall_group', 'security', 'readonly', 'enabled',
            ]
            for key in _fields:
                if module.params.get(key) is not None:
                    api_key = _field_map.get(key, key)
                    payload[api_key] = module.params[key]

            if existing:
                changes = {}
                for key, value in payload.items():
                    existing_val = existing.get(key)
                    # Treat None and empty string as equivalent for string fields
                    if isinstance(value, str) or value is None:
                        if _normalize_value(existing_val) != _normalize_value(value):
                            changes[key] = value
                    elif existing_val != value:
                        changes[key] = value
                if changes:
                    if not module.check_mode:
                        existing = client.put(
                            "sharing/nfs/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["nfs_share"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("sharing/nfs", payload)
                result["changed"] = True
                result["nfs_share"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
