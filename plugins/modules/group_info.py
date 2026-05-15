#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: group_info
short_description: Gather group information
version_added: "1.1.0"
description:
  - Retrieve group information from a TrueNAS system via the middleware API.
options:
  group_name:
    description: Group name to filter results. Uses C(group_name) to avoid collision with Ansible's C(group) keyword.
    type: str
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: List all groups
  stevefulme1.truenas.group_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"

- name: Get a specific group
  stevefulme1.truenas.group_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    group_name: wheel
"""

RETURN = r"""
groups:
  description: List of groups.
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
        group_name=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    group_name = module.params.get("group_name")

    try:
        data = client.get("group")
        groups = data if isinstance(data, list) else [data]

        if group_name:
            groups = [g for g in groups if g.get("group") == group_name]

        module.exit_json(changed=False, groups=groups)
    except TrueNASError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
