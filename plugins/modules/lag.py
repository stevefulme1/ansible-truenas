#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: lag
short_description: Create or modify link aggregation groups
version_added: "1.0.0"
description:
  - Create or modify link aggregation groups on a TrueNAS system via the middleware API.
options:
  name:
    description: LAG interface name
    type: str
    required: true
  protocol:
    description: LAG protocol
    type: str
    default: LACP
    choices: ['LACP', 'FAILOVER', 'LOADBALANCE', 'ROUNDROBIN', 'NONE']
  members:
    description: Member interface names
    type: list
    required: true
  ipv4_addresses:
    description: IPv4 addresses
    type: list
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
- name: Manage create or modify link aggregation groups
  truenas.storage.lag:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: example_value
    members:
      - item1
"""

RETURN = r"""
lag:
  description: The create or modify link aggregation groups details.
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
        protocol=dict(type="str", default="LACP", choices=['LACP', 'FAILOVER', 'LOADBALANCE', 'ROUNDROBIN', 'NONE']),
        members=dict(type="list", required=True),
        ipv4_addresses=dict(type="list"),
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
            for key in ['name', 'protocol', 'members', 'ipv4_addresses', 'mtu']:
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
                result["lag"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("interface", payload)
                result["changed"] = True
                result["lag"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
