#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ldap
short_description: Configure LDAP directory service
version_added: "1.0.0"
description:
  - Configure LDAP directory service on a TrueNAS system via the middleware API.
options:
  hostname:
    description: LDAP server hostnames
    type: list
    elements: str
    required: true
  basedn:
    description: Base DN
    type: str
    required: true
  binddn:
    description: Bind DN
    type: str
  bindpw:
    description: Bind password
    type: str
  ssl:
    description: SSL mode
    type: str
    default: "ON"
    choices: ['OFF', 'ON', 'START_TLS']
  certificate:
    description: Certificate ID
    type: int
  schema:
    description: LDAP schema
    type: str
    choices: ['RFC2307', 'RFC2307BIS']
  enable:
    description: Enable LDAP
    type: bool
    default: True
extends_documentation_fragment:
  - truenas.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure ldap directory service
  truenas.storage.ldap:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    hostname:
      - item1
    basedn: example_value
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
        hostname=dict(type="list", elements="str", required=True),
        basedn=dict(type="str", required=True),
        binddn=dict(type="str"),
        bindpw=dict(type="str", no_log=True),
        ssl=dict(type="str", default="ON", choices=['OFF', 'ON', 'START_TLS']),
        certificate=dict(type="int"),
        schema=dict(type="str", choices=['RFC2307', 'RFC2307BIS']),
        enable=dict(type="bool", default=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        current = client.get("ldap")
        payload = {}
        if module.params["hostname"] is not None and current.get("hostname") != module.params["hostname"]:
            payload["hostname"] = module.params["hostname"]
        if module.params["basedn"] is not None and current.get("basedn") != module.params["basedn"]:
            payload["basedn"] = module.params["basedn"]
        if module.params["binddn"] is not None and current.get("binddn") != module.params["binddn"]:
            payload["binddn"] = module.params["binddn"]
        if module.params["bindpw"] is not None:
            payload["bindpw"] = module.params["bindpw"]
        if module.params["ssl"] is not None and current.get("ssl") != module.params["ssl"]:
            payload["ssl"] = module.params["ssl"]
        if module.params["certificate"] is not None and current.get("certificate") != module.params["certificate"]:
            payload["certificate"] = module.params["certificate"]
        if module.params["schema"] is not None and current.get("schema") != module.params["schema"]:
            payload["schema"] = module.params["schema"]
        if module.params["enable"] is not None and current.get("enable") != module.params["enable"]:
            payload["enable"] = module.params["enable"]
        if payload:
            if not module.check_mode:
                current = client.put("ldap", payload)
            result["changed"] = True
        result["config"] = current
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
