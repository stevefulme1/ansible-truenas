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
options:
  path:
    description: Filesystem path to export
    type: str
  paths:
    description: List of paths to export
    type: list
  comment:
    description: Export description
    type: str
  networks:
    description: Authorized networks (CIDR)
    type: list
  hosts:
    description: Authorized hosts
    type: list
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
  readonly:
    description: Read-only export
    type: bool
    default: False
  enabled:
    description: Enable the export
    type: bool
    default: True
  state:
    description: Desired state of the resource.
    type: str
    choices: [present, absent]
    default: present
extends_documentation_fragment:
  - truenas.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage manage nfs exports
  truenas.storage.nfs_share:
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
from ansible_collections.truenas.storage.plugins.module_utils.truenas_api import (
    TrueNASClient,
    TrueNASError,
    truenas_argument_spec,
)


def main():
    argument_spec = truenas_argument_spec()
    argument_spec.update(
        path=dict(type="str"),
        paths=dict(type="list"),
        comment=dict(type="str"),
        networks=dict(type="list"),
        hosts=dict(type="list"),
        maproot_user=dict(type="str"),
        maproot_group=dict(type="str"),
        mapall_user=dict(type="str"),
        mapall_group=dict(type="str"),
        security=dict(type="list"),
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
            for item in items:
                if item.get("path") == module.params.get("path"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("sharing/nfs/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['path', 'paths', 'comment', 'networks', 'hosts', 'maproot_user', 'maproot_group', 'mapall_user', 'mapall_group', 'security', 'readonly', 'enabled']:
                if module.params.get(key) is not None:
                    payload[key] = module.params[key]

            if existing:
                changes = {}
                for key, value in payload.items():
                    if existing.get(key) != value:
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
