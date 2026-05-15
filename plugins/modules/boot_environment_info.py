#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: boot_environment_info
short_description: Gather boot environment information
version_added: "1.1.0"
description:
  - Retrieve boot environment information from a TrueNAS system via the middleware API.
options:
  name:
    description: Boot environment name to filter results.
    type: str
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: List all boot environments
  stevefulme1.truenas.boot_environment_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"

- name: Get a specific boot environment
  stevefulme1.truenas.boot_environment_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: default
"""

RETURN = r"""
boot_environments:
  description: List of boot environments.
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
        name=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    name = module.params.get("name")

    try:
        data = client.get("bootenv")
        boot_environments = data if isinstance(data, list) else [data]

        if name:
            boot_environments = [
                b for b in boot_environments if b.get("name") == name
            ]

        module.exit_json(changed=False, boot_environments=boot_environments)
    except TrueNASError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
