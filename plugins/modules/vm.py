#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: vm
short_description: Manage virtual machines
version_added: "1.0.0"
description:
  - Manage virtual machines on a TrueNAS system via the middleware API.
options:
  name:
    description: VM name
    type: str
    required: true
  vcpus:
    description: Number of virtual CPUs
    type: int
    default: 1
  memory:
    description: Memory in MiB
    type: int
  autostart:
    description: Start on boot
    type: bool
    default: False
  bootloader:
    description: Bootloader type
    type: str
    default: UEFI
    choices: ['UEFI', 'UEFI_CSM']
  devices:
    description: VM devices (disks, NICs, CDROMs)
    type: list
    elements: str
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
- name: Create a virtual machine
  stevefulme1.truenas.vm:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: ubuntu-server
    vcpus: 2
    memory: 4096
    bootloader: UEFI
    autostart: true
    state: present

- name: Create a lightweight VM for testing
  stevefulme1.truenas.vm:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: test-vm
    vcpus: 1
    memory: 1024
    bootloader: UEFI
    autostart: false
    state: present

- name: Remove a virtual machine
  stevefulme1.truenas.vm:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: old-vm
    state: absent
"""

RETURN = r"""
vm:
  description: The manage virtual machines details.
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
        vcpus=dict(type="int", default=1),
        memory=dict(type="int"),
        autostart=dict(type="bool", default=False),
        bootloader=dict(type="str", default="UEFI", choices=['UEFI', 'UEFI_CSM']),
        devices=dict(type="list", elements="str"),
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
        items = client.get("vm")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("vm/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['name', 'vcpus', 'memory', 'autostart', 'bootloader', 'devices']:
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
                            "vm/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["vm"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("vm", payload)
                result["changed"] = True
                result["vm"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
