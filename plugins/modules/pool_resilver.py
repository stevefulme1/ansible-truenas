#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: pool_resilver
short_description: Configure pool resilver priority
version_added: "1.0.0"
description:
  - Configure pool resilver priority on a TrueNAS system via the middleware API.
options:
  enabled:
    description: Enable resilver priority schedule
    type: bool
    default: False
  begin:
    description: Start time for priority resilver
    type: str
    default: "18:00"
  end:
    description: End time for priority resilver
    type: str
    default: "09:00"
  weekday:
    description: Days of the week (1-7)
    type: list
    elements: str
extends_documentation_fragment:
  - truenas.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure pool resilver priority
  truenas.storage.pool_resilver:
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
        enabled=dict(type="bool", default=False),
        begin=dict(type="str", default="18:00"),
        end=dict(type="str", default="09:00"),
        weekday=dict(type="list", elements="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        current = client.get("pool/resilver")
        payload = {}
        if module.params["enabled"] is not None and current.get("enabled") != module.params["enabled"]:
            payload["enabled"] = module.params["enabled"]
        if module.params["begin"] is not None and current.get("begin") != module.params["begin"]:
            payload["begin"] = module.params["begin"]
        if module.params["end"] is not None and current.get("end") != module.params["end"]:
            payload["end"] = module.params["end"]
        if module.params["weekday"] is not None and current.get("weekday") != module.params["weekday"]:
            payload["weekday"] = module.params["weekday"]
        if payload:
            if not module.check_mode:
                current = client.put("pool/resilver", payload)
            result["changed"] = True
        result["config"] = current
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
