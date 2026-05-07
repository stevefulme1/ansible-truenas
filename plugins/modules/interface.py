#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: interface
short_description: Configure network interfaces
version_added: "1.0.0"
description:
  - Configure network interfaces on a TrueNAS system via the middleware API.
options:
  name:
    description: Interface name
    type: str
    required: true
  ipv4_dhcp:
    description: Enable DHCP
    type: bool
  ipv4_addresses:
    description: IPv4 addresses with netmask
    type: list
    elements: str
  ipv6_auto:
    description: Enable IPv6 auto-configuration
    type: bool
  ipv6_addresses:
    description: IPv6 addresses with prefix length
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
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Configure a network interface with a static IP
  stevefulme1.truenas.interface:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: eno1
    ipv4_dhcp: false
    ipv4_addresses:
      - "192.168.1.100/24"
    mtu: 9000
    state: present

- name: Configure a network interface with DHCP
  stevefulme1.truenas.interface:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: eno1
    ipv4_dhcp: true
    state: present
"""

RETURN = r"""
interface:
  description: The configure network interfaces details.
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
        name=dict(type="str", required=True),
        ipv4_dhcp=dict(type="bool"),
        ipv4_addresses=dict(type="list", elements="str"),
        ipv6_auto=dict(type="bool"),
        ipv6_addresses=dict(type="list", elements="str"),
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
            for key in ['name', 'ipv4_dhcp', 'ipv4_addresses', 'ipv6_auto', 'ipv6_addresses', 'mtu']:
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
                result["interface"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("interface", payload)
                result["changed"] = True
                result["interface"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
