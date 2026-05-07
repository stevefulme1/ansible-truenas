#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: smb_config
short_description: Configure global SMB service settings
version_added: "1.0.0"
description:
  - Configure global SMB service settings on a TrueNAS system via the middleware API.
options:
  workgroup:
    description: SMB workgroup name
    type: str
  description:
    description: Server description
    type: str
  enable_smb1:
    description: Enable SMB1 protocol
    type: bool
    default: False
  ntlmv1_auth:
    description: Allow NTLMv1 authentication
    type: bool
    default: False
  multichannel:
    description: Enable SMB multichannel
    type: bool
    default: False
  unix_charset:
    description: Unix character set
    type: str
    default: UTF-8
  loglevel:
    description: Log level
    type: str
    choices: ['NONE', 'MINIMUM', 'NORMAL', 'FULL', 'DEBUG']
extends_documentation_fragment:
  - stevefulme1.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure global smb service settings
  stevefulme1.storage.smb_config:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    state: present
"""

RETURN = r"""
config:
  description: Current configuration.
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
        workgroup=dict(type="str"),
        description=dict(type="str"),
        enable_smb1=dict(type="bool", default=False),
        ntlmv1_auth=dict(type="bool", default=False),
        multichannel=dict(type="bool", default=False),
        unix_charset=dict(type="str", default="UTF-8"),
        loglevel=dict(type="str", choices=['NONE', 'MINIMUM', 'NORMAL', 'FULL', 'DEBUG']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        current = client.get("smb")
        payload = {}
        if module.params["workgroup"] is not None and current.get("workgroup") != module.params["workgroup"]:
            payload["workgroup"] = module.params["workgroup"]
        if module.params["description"] is not None and current.get("description") != module.params["description"]:
            payload["description"] = module.params["description"]
        if module.params["enable_smb1"] is not None and current.get("enable_smb1") != module.params["enable_smb1"]:
            payload["enable_smb1"] = module.params["enable_smb1"]
        if module.params["ntlmv1_auth"] is not None and current.get("ntlmv1_auth") != module.params["ntlmv1_auth"]:
            payload["ntlmv1_auth"] = module.params["ntlmv1_auth"]
        if module.params["multichannel"] is not None and current.get("multichannel") != module.params["multichannel"]:
            payload["multichannel"] = module.params["multichannel"]
        if module.params["unix_charset"] is not None and current.get("unix_charset") != module.params["unix_charset"]:
            payload["unix_charset"] = module.params["unix_charset"]
        if module.params["loglevel"] is not None and current.get("loglevel") != module.params["loglevel"]:
            payload["loglevel"] = module.params["loglevel"]
        if payload:
            if not module.check_mode:
                current = client.put("smb", payload)
            result["changed"] = True
        result["config"] = current
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
