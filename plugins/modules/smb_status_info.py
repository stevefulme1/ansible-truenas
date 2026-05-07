#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: smb_status_info
short_description: Gather SMB service status and active sessions
version_added: "1.0.0"
description:
  - Gather SMB service status and active sessions from a TrueNAS system via the middleware API.
options:
  {}
extends_documentation_fragment:
  - truenas.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage gather smb service status and active sessions
  truenas.storage.smb_status_info:
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
from ansible_collections.truenas.storage.plugins.module_utils.truenas_api import (
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

    try:
        data = client.get("smb/status")
        module.exit_json(changed=False, data=data)
    except TrueNASError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
