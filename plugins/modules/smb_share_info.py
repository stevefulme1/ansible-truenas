#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: smb_share_info
short_description: Gather SMB share information
version_added: "1.0.0"
description:
  - Gather SMB share information from a TrueNAS system via the middleware API.
  - This is a read-only module.
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Get SMB share information
  stevefulme1.truenas.smb_share_info:
    api_url: "https://truenas.example.com"
    api_key: "{ truenas_api_key }"
  register: result
"""

RETURN = r"""
smb_shares:
  description: The SMB share information.
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
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        data = client.get("sharing/smb")
        result["smb_shares"] = data
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
