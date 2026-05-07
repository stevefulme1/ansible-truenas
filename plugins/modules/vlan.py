#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: vlan
short_description: Create or modify VLAN interfaces
version_added: "1.0.0"
description:
  - Create or modify VLAN interfaces on a TrueNAS system via the middleware API.
options:
  name:
    description: VLAN interface name
    type: str
    required: true
  parent_interface:
    description: Parent physical interface
    type: str
    required: true
  tag:
    description: VLAN tag (1-4094)
    type: int
    required: true
  pcp:
    description: Priority code point
    type: int
  ipv4_addresses:
    description: IPv4 addresses
    type: list
    elements: str
  mtu:
    description: MTU size
    type: int
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
- name: Manage create or modify vlan interfaces
  truenas.storage.vlan:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: example_value
    parent_interface: example_value
    tag: 1
"""

RETURN = r"""
vlan:
  description: The create or modify vlan interfaces details.
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
        name=dict(type="str", required=True),
        parent_interface=dict(type="str", required=True),
        tag=dict(type="int", required=True),
        pcp=dict(type="int"),
        ipv4_addresses=dict(type="list", elements="str"),
        mtu=dict(type="int"),
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
        items = client.get("interface")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("interface/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['name', 'parent_interface', 'tag', 'pcp', 'ipv4_addresses', 'mtu']:
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
                            "interface/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["vlan"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("interface", payload)
                result["changed"] = True
                result["vlan"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
