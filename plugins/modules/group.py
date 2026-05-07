#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: group
short_description: Manage local groups
version_added: "1.0.0"
description:
  - Manage local groups on a TrueNAS system via the middleware API.
options:
  name:
    description: Group name
    type: str
    required: true
  gid:
    description: Group ID
    type: int
  sudo_commands:
    description: Allowed sudo commands
    type: list
    elements: str
  smb:
    description: SMB group
    type: bool
    default: true
  allow_duplicate_gid:
    description: Allow creating groups with non-unique GIDs
    type: bool
    default: false
  users:
    description: List of usernames to add to the group
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
- name: Create a group for developers
  stevefulme1.truenas.group:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: developers
    smb: true
    users:
      - john
      - smbuser
    state: present

- name: Create a group with sudo access
  stevefulme1.truenas.group:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: backup-operators
    smb: false
    sudo_commands:
      - /usr/local/bin/rsync
      - /sbin/zfs
    state: present

- name: Remove a group
  stevefulme1.truenas.group:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: old-team
    state: absent
"""

RETURN = r"""
group:
  description: The manage local groups details.
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
        gid=dict(type="int"),
        sudo_commands=dict(type="list", elements="str"),
        smb=dict(type="bool", default=True),
        allow_duplicate_gid=dict(type="bool", default=False),
        users=dict(type="list", elements="str"),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    client = TrueNASClient(module)
    state = module.params["state"]
    result = dict(changed=False)

    try:
        existing = None
        items = client.get("group")
        if isinstance(items, list):
            for item in items:
                if item.get("group") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("group/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            _fields = [
                'name', 'gid', 'sudo_commands', 'smb',
                'allow_duplicate_gid', 'users',
            ]
            for key in _fields:
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
                            "group/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["group"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("group", payload)
                result["changed"] = True
                result["group"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
