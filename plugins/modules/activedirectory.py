#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: activedirectory
short_description: Join or leave an Active Directory domain
version_added: "1.0.0"
description:
  - Join or leave an Active Directory domain on a TrueNAS system via the middleware API.
options:
  domainname:
    description: AD domain name
    type: str
    required: true
  bindname:
    description: AD bind username
    type: str
  bindpw:
    description: AD bind password
    type: str
  site:
    description: AD site name
    type: str
  kerberos_realm:
    description: Kerberos realm
    type: str
  kerberos_principal:
    description: Kerberos principal
    type: str
  enable:
    description: Enable Active Directory
    type: bool
    default: True
extends_documentation_fragment:
  - truenas.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage join or leave an active directory domain
  truenas.storage.activedirectory:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    domainname: example_value
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
        domainname=dict(type="str", required=True),
        bindname=dict(type="str"),
        bindpw=dict(type="str", no_log=True),
        site=dict(type="str"),
        kerberos_realm=dict(type="str"),
        kerberos_principal=dict(type="str"),
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
        current = client.get("activedirectory")
        payload = {}
        if module.params["domainname"] is not None and current.get("domainname") != module.params["domainname"]:
            payload["domainname"] = module.params["domainname"]
        if module.params["bindname"] is not None and current.get("bindname") != module.params["bindname"]:
            payload["bindname"] = module.params["bindname"]
        if module.params["bindpw"] is not None and current.get("bindpw") != module.params["bindpw"]:
            payload["bindpw"] = module.params["bindpw"]
        if module.params["site"] is not None and current.get("site") != module.params["site"]:
            payload["site"] = module.params["site"]
        if module.params["kerberos_realm"] is not None and current.get("kerberos_realm") != module.params["kerberos_realm"]:
            payload["kerberos_realm"] = module.params["kerberos_realm"]
        if module.params["kerberos_principal"] is not None and current.get("kerberos_principal") != module.params["kerberos_principal"]:
            payload["kerberos_principal"] = module.params["kerberos_principal"]
        if module.params["enable"] is not None and current.get("enable") != module.params["enable"]:
            payload["enable"] = module.params["enable"]
        if payload:
            if not module.check_mode:
                current = client.put("activedirectory", payload)
            result["changed"] = True
        result["config"] = current
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
