#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: failover
short_description: Control HA failover
version_added: "1.0.0"
description:
  - Control HA failover on a TrueNAS system via the middleware API.
options:
  action:
    description: Failover action
    type: str
    choices: ['enable', 'disable', 'trigger']
  master:
    description: Whether this node should be master
    type: bool
  timeout:
    description: Failover timeout in seconds
    type: int
    default: 60
  disabled_reasons:
    description: Reasons to display when disabled
    type: list
    elements: str
extends_documentation_fragment:
  - truenas.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage control ha failover
  truenas.storage.failover:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    state: present
"""

RETURN = r"""
result:
  description: Action result.
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
        action=dict(type="str", choices=['enable', 'disable', 'trigger']),
        master=dict(type="bool"),
        timeout=dict(type="int", default=60),
        disabled_reasons=dict(type="list", elements="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        if not module.check_mode:
            response = client.post("failover", {
                "action": module.params["action"],
                "master": module.params["master"],
                "timeout": module.params["timeout"],
                "disabled_reasons": module.params["disabled_reasons"],
            })
            result["result"] = response
        result["changed"] = True
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
