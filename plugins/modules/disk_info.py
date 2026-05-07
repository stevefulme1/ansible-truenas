#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: disk_info
short_description: Gather disk information
version_added: "1.0.0"
description:
  - Gather disk information from a TrueNAS system via the middleware API.
options:
  name:
    description: Specific disk name to query
    type: str
extends_documentation_fragment:
  - stevefulme1.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage gather disk information
  stevefulme1.storage.disk_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
"""

RETURN = r"""
data:
  description: Retrieved information.
  returned: success
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.storage.plugins.module_utils.truenas_api import (
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

    try:
        data = client.get("disk")
        module.exit_json(changed=False, data=data)
    except TrueNASError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
