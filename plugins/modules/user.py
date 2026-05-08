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
  password_disabled:
    description:
      - When true, the user has no password and cannot log in with one.
      - Mutually exclusive with providing a password.
    type: bool
    default: false
  smb:
    description:
      - Enable Samba authentication for this user.
      - Automatically set to false when I(password_disabled=true).
    type: bool
    default: true
  uid:
    description: User ID
    type: int
  group:
    description: Primary group name
    type: str
  groups:
    description: Additional group names
    type: list
    elements: str
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
    elements: str
  sudo_commands_nopasswd:
    description: Commands the user can sudo without a password
    type: list
    elements: str
  locked:
    description: Lock the account
    type: bool
    default: false
  microsoft_account:
    description: Link to a Microsoft account (SCALE)
    type: bool
  roles:
    description:
      - List of RBAC roles to assign to the user (TrueNAS SCALE 24.10+).
      - "Example roles: FULL_ADMIN, READONLY_ADMIN, SHARING_ADMIN."
    type: list
    elements: str
  update_password:
    description:
      - When to update the password.
      - C(always) updates password every run if provided.
      - C(on_create) only sets password when creating a new user.
    type: str
    choices: [always, on_create]
    default: always
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
- name: Create a local user for SMB access
  stevefulme1.truenas.user:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    username: john
    full_name: John Smith
    email: john@example.com
    password: "{{ vault_user_password }}"
    group: developers
    groups:
      - media
    home: /mnt/tank/home/john
    shell: /usr/bin/bash
    smb: true
    state: present

- name: Create a service account without password login
  stevefulme1.truenas.user:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    username: backupuser
    full_name: Backup Service Account
    password_disabled: true
    group: backup-operators
    sshpubkey: "{{ lookup('file', '~/.ssh/backup_key.pub') }}"
    shell: /usr/sbin/nologin
    state: present

- name: Remove a user
  stevefulme1.truenas.user:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    username: former-employee
    state: absent
"""

RETURN = r"""
user:
  description: The manage local users details.
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
        username=dict(type="str", required=True),
        full_name=dict(type="str"),
        email=dict(type="str"),
        password=dict(type="str", no_log=True),
        password_disabled=dict(type="bool", default=False),
        smb=dict(type="bool", default=True),
        uid=dict(type="int"),
        group=dict(type="str"),
        groups=dict(type="list", elements="str"),
        home=dict(type="str"),
        shell=dict(type="str"),
        sshpubkey=dict(type="str"),
        sudo_commands=dict(type="list", elements="str"),
        sudo_commands_nopasswd=dict(type="list", elements="str", no_log=False),
        locked=dict(type="bool", default=False),
        microsoft_account=dict(type="bool"),
        roles=dict(type="list", elements="str"),
        update_password=dict(
            type="str", choices=["always", "on_create"], default="always",
        ),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
        mutually_exclusive=[["password", "password_disabled"]],
    )

    client = TrueNASClient(module)
    state = module.params["state"]
    result = dict(changed=False)

    # When password_disabled is true, smb must be false and password must not be sent
    password_disabled = module.params.get("password_disabled")
    if password_disabled:
        module.params["smb"] = False

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
            _fields = [
                'username', 'full_name', 'email', 'uid', 'group', 'groups',
                'home', 'shell', 'sshpubkey', 'sudo_commands',
                'sudo_commands_nopasswd', 'locked', 'password_disabled',
                'smb', 'microsoft_account', 'roles',
            ]
            for key in _fields:
                if module.params.get(key) is not None:
                    payload[key] = module.params[key]

            update_password = module.params.get("update_password", "always")

            if existing:
                changes = {}
                for key, value in payload.items():
                    if existing.get(key) != value:
                        changes[key] = value
                # Only include password on update when update_password=always
                if (
                    not password_disabled
                    and module.params.get("password") is not None
                    and update_password == "always"
                ):
                    changes["password"] = module.params["password"]
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
                _sensitive_keys = {'password'}
                safe_payload = {k: v for k, v in payload.items() if k not in _sensitive_keys}
                result["user"] = existing or safe_payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
