#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: user_info
short_description: Gather user account information
version_added: "1.1.0"
description:
  - Retrieve user account information from a TrueNAS system via the middleware API.
options:
  username:
    description: Username to filter results.
    type: str
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: List all users
  stevefulme1.truenas.user_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"

- name: Get a specific user
  stevefulme1.truenas.user_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    username: admin
"""

RETURN = r"""
users:
  description: List of user accounts.
  returned: success
  type: list
  elements: dict
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
        username=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    username = module.params.get("username")

    try:
        data = client.get("user")
        users = data if isinstance(data, list) else [data]

        if username:
            users = [u for u in users if u.get("username") == username]

        module.exit_json(changed=False, users=users)
    except TrueNASError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
