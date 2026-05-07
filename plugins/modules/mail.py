#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: mail
short_description: Configure email notification settings
version_added: "1.0.0"
description:
  - Configure email notification settings on a TrueNAS system via the middleware API.
options:
  fromemail:
    description: From email address
    type: str
  outgoingserver:
    description: SMTP server hostname
    type: str
  port:
    description: SMTP port
    type: int
    default: 587
  security:
    description: Connection security
    type: str
    default: TLS
    choices: ['PLAIN', 'SSL', 'TLS']
  smtp:
    description: Enable SMTP authentication
    type: bool
    default: True
  user:
    description: SMTP username
    type: str
  pass_value:
    description: SMTP password
    type: str
extends_documentation_fragment:
  - truenas.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure email notification settings
  truenas.storage.mail:
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
        fromemail=dict(type="str"),
        outgoingserver=dict(type="str"),
        port=dict(type="int", default=587),
        security=dict(type="str", default="TLS", choices=['PLAIN', 'SSL', 'TLS']),
        smtp=dict(type="bool", default=True),
        user=dict(type="str"),
        pass_value=dict(type="str", no_log=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        current = client.get("mail")
        payload = {}
        if module.params["fromemail"] is not None and current.get("fromemail") != module.params["fromemail"]:
            payload["fromemail"] = module.params["fromemail"]
        if module.params["outgoingserver"] is not None and current.get("outgoingserver") != module.params["outgoingserver"]:
            payload["outgoingserver"] = module.params["outgoingserver"]
        if module.params["port"] is not None and current.get("port") != module.params["port"]:
            payload["port"] = module.params["port"]
        if module.params["security"] is not None and current.get("security") != module.params["security"]:
            payload["security"] = module.params["security"]
        if module.params["smtp"] is not None and current.get("smtp") != module.params["smtp"]:
            payload["smtp"] = module.params["smtp"]
        if module.params["user"] is not None and current.get("user") != module.params["user"]:
            payload["user"] = module.params["user"]
        if module.params["pass_value"] is not None and current.get("pass_value") != module.params["pass_value"]:
            payload["pass_value"] = module.params["pass_value"]
        if payload:
            if not module.check_mode:
                current = client.put("mail", payload)
            result["changed"] = True
        result["config"] = current
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
