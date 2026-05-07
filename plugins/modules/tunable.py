#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: tunable
short_description: Manage system tunables
version_added: "1.0.0"
description:
  - Manage system tunables on a TrueNAS system via the middleware API.
options:
  var:
    description: Variable name
    type: str
    required: true
  value:
    description: Variable value
    type: str
    required: true
  type:
    description: Tunable type
    type: str
    default: SYSCTL
    choices: ['SYSCTL', 'UDEV']
  comment:
    description: Description
    type: str
  enabled:
    description: Enable the tunable
    type: bool
    default: True
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
- name: Set a sysctl tunable for network performance
  stevefulme1.truenas.tunable:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    var: net.core.rmem_max
    value: "16777216"
    type: SYSCTL
    comment: Increase receive buffer size for NFS performance
    state: present

- name: Set a ZFS tunable
  stevefulme1.truenas.tunable:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    var: zfs.zfs_arc_max
    value: "8589934592"
    type: SYSCTL
    comment: Limit ARC to 8GB
    state: present

- name: Remove a tunable
  stevefulme1.truenas.tunable:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    var: net.core.rmem_max
    value: "16777216"
    state: absent
"""

RETURN = r"""
tunable:
  description: The manage system tunables details.
  returned: success
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
    TrueNASClient,
    TrueNASError,
    truenas_argument_spec,
)


def main():
    argument_spec = truenas_argument_spec()
    argument_spec.update(
        var=dict(type="str", required=True),
        value=dict(type="str", required=True),
        type=dict(type="str", default="SYSCTL", choices=['SYSCTL', 'UDEV']),
        comment=dict(type="str"),
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
        items = client.get("tunable")
        if isinstance(items, list):
            for item in items:
                if item.get("var") == module.params.get("var"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("tunable/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['var', 'value', 'type', 'comment', 'enabled']:
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
                            "tunable/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["tunable"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("tunable", payload)
                result["changed"] = True
                result["tunable"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
