#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: smb_share_info
short_description: Gather SMB share information
version_added: "1.1.0"
description:
  - Retrieve SMB share configuration from a TrueNAS system via the middleware API.
options:
  name:
    description: Share name to filter results.
    type: str
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: List all SMB shares
  stevefulme1.truenas.smb_share_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"

- name: Get a specific SMB share
  stevefulme1.truenas.smb_share_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: data
"""

RETURN = r"""
shares:
  description: List of SMB shares.
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
        data = client.get("sharing/smb")
        shares = data if isinstance(data, list) else [data]

        if name:
            shares = [s for s in shares if s.get("name") == name]

        module.exit_json(changed=False, shares=shares)
    except TrueNASError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
