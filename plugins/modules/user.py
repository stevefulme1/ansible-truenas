#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: user
short_description: Manage local users
version_added: "1.0.0"
description:
  - Manage local users on a TrueNAS system via the middleware API.
options:
  username:
    description: Username
    type: str
    required: true
  full_name:
    description: Full name
    type: str
  email:
    description: Email address
    type: str
  password:
    description: User password
    type: str
  uid:
    description: User ID
    type: int
  group:
    description: Primary group name
    type: str
  groups:
    description: Additional group names
    type: list
  home:
    description: Home directory path
    type: str
  shell:
    description: Login shell
    type: str
  sshpubkey:
    description: SSH public key
    type: str
  sudo_commands:
    description: Allowed sudo commands
    type: list
  locked:
    description: Lock the account
    type: bool
    default: False
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
- name: Manage manage local users
  truenas.storage.user:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    username: example_value
"""

RETURN = r"""
user:
  description: The manage local users details.
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
        username=dict(type="str", required=True),
        full_name=dict(type="str"),
        email=dict(type="str"),
        password=dict(type="str", no_log=True),
        uid=dict(type="int"),
        group=dict(type="str"),
        groups=dict(type="list"),
        home=dict(type="str"),
        shell=dict(type="str"),
        sshpubkey=dict(type="str"),
        sudo_commands=dict(type="list"),
        locked=dict(type="bool", default=False),
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
        items = client.get("user")
        if isinstance(items, list):
            for item in items:
                if item.get("username") == module.params.get("username"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("user/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['username', 'full_name', 'email', 'password', 'uid', 'group', 'groups', 'home', 'shell', 'sshpubkey', 'sudo_commands', 'locked']:
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
                            "user/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["user"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("user", payload)
                result["changed"] = True
                result["user"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
