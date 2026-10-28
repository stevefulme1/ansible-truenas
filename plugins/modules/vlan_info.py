#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: vlan_info
short_description: Gather VLAN interface information
version_added: "1.0.0"
description:
  - Gather VLAN interface information from a TrueNAS system via the middleware API.
  - This is a read-only module.
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Get VLAN interface information
  stevefulme1.truenas.vlan_info:
    api_url: "https://truenas.example.com"
    api_key: "{ truenas_api_key }"
  register: result
"""

RETURN = r"""
vlans:
  description: The VLAN interface information.
  returned: success
  type: list
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
    TrueNASClient,
    TrueNASError,
    truenas_argument_spec,
)


def main():
    argument_spec = truenas_argument_spec()

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "api_username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        data = client.get("interface")
        result["vlans"] = data
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
