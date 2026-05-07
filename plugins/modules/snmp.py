#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: snmp
short_description: Configure SNMP service
version_added: "1.0.0"
description:
  - Configure SNMP service on a TrueNAS system via the middleware API.
options:
  community:
    description: SNMP community string
    type: str
    default: public
  contact:
    description: System contact
    type: str
  location:
    description: System location
    type: str
  v3:
    description: Enable SNMPv3
    type: bool
    default: False
  v3_username:
    description: SNMPv3 username
    type: str
  v3_authtype:
    description: SNMPv3 auth type
    type: str
    choices: ['MD5', 'SHA']
  v3_password:
    description: SNMPv3 auth password
    type: str
  v3_privproto:
    description: SNMPv3 privacy protocol
    type: str
    choices: ['AES', 'DES']
  v3_privpassphrase:
    description: SNMPv3 privacy passphrase
    type: str
extends_documentation_fragment:
  - truenas.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure snmp service
  truenas.storage.snmp:
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
from ansible_collections.truenas.storage.plugins.module_utils.truenas_api import (
    TrueNASClient,
    TrueNASError,
    truenas_argument_spec,
)


def main():
    argument_spec = truenas_argument_spec()
    argument_spec.update(
        community=dict(type="str", default="public"),
        contact=dict(type="str"),
        location=dict(type="str"),
        v3=dict(type="bool", default=False),
        v3_username=dict(type="str"),
        v3_authtype=dict(type="str", choices=['MD5', 'SHA']),
        v3_password=dict(type="str", no_log=True),
        v3_privproto=dict(type="str", choices=['AES', 'DES']),
        v3_privpassphrase=dict(type="str", no_log=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        current = client.get("snmp")
        payload = {}
        if module.params["community"] is not None and current.get("community") != module.params["community"]:
            payload["community"] = module.params["community"]
        if module.params["contact"] is not None and current.get("contact") != module.params["contact"]:
            payload["contact"] = module.params["contact"]
        if module.params["location"] is not None and current.get("location") != module.params["location"]:
            payload["location"] = module.params["location"]
        if module.params["v3"] is not None and current.get("v3") != module.params["v3"]:
            payload["v3"] = module.params["v3"]
        if module.params["v3_username"] is not None and current.get("v3_username") != module.params["v3_username"]:
            payload["v3_username"] = module.params["v3_username"]
        if module.params["v3_authtype"] is not None and current.get("v3_authtype") != module.params["v3_authtype"]:
            payload["v3_authtype"] = module.params["v3_authtype"]
        if module.params["v3_password"] is not None:
            payload["v3_password"] = module.params["v3_password"]
        if module.params["v3_privproto"] is not None and current.get("v3_privproto") != module.params["v3_privproto"]:
            payload["v3_privproto"] = module.params["v3_privproto"]
        if module.params["v3_privpassphrase"] is not None:
            payload["v3_privpassphrase"] = module.params["v3_privpassphrase"]
        if payload:
            if not module.check_mode:
                current = client.put("snmp", payload)
            result["changed"] = True
        result["config"] = current
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
