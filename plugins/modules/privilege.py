#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: privilege
short_description: Manage admin privileges and roles
version_added: "1.0.0"
description:
  - Manage admin privileges and roles on a TrueNAS system via the middleware API.
options:
  name:
    description: Privilege name
    type: str
    required: true
  local_groups:
    description: Local groups with this privilege
    type: list
    elements: str
  ds_groups:
    description: Directory service groups with this privilege
    type: list
    elements: str
  roles:
    description: Roles to assign
    type: list
    elements: str
  web_shell:
    description: Allow web shell access
    type: bool
    default: False
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
- name: Create a read-only admin privilege
  stevefulme1.truenas.privilege:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: monitoring-access
    local_groups:
      - developers
    roles:
      - READONLY_ADMIN
    web_shell: false
    state: present

- name: Create a full admin privilege for operators
  stevefulme1.truenas.privilege:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: operator-access
    local_groups:
      - backup-operators
    ds_groups:
      - Domain Admins
    roles:
      - FULL_ADMIN
    web_shell: true
    state: present

- name: Remove a privilege
  stevefulme1.truenas.privilege:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: old-privilege
    state: absent
"""

RETURN = r"""
privilege:
  description: The manage admin privileges and roles details.
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
        local_groups=dict(type="list", elements="str"),
        ds_groups=dict(type="list", elements="str"),
        roles=dict(type="list", elements="str"),
        web_shell=dict(type="bool", default=False),
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
        items = client.get("privilege")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("privilege/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['name', 'local_groups', 'ds_groups', 'roles', 'web_shell']:
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
                            "privilege/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["privilege"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("privilege", payload)
                result["changed"] = True
                result["privilege"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
