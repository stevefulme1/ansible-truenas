#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ntp
short_description: Manage NTP servers
version_added: "1.0.0"
description:
  - Manage NTP servers on a TrueNAS system via the middleware API.
options:
  address:
    description: NTP server address
    type: str
    required: true
  burst:
    description: Enable burst mode
    type: bool
    default: False
  iburst:
    description: Enable initial burst
    type: bool
    default: True
  prefer:
    description: Prefer this server
    type: bool
    default: False
  minpoll:
    description: Minimum poll interval (power of 2)
    type: int
    default: 6
  maxpoll:
    description: Maximum poll interval (power of 2)
    type: int
    default: 10
  state:
    description: Desired state of the resource.
    type: str
    choices: [present, absent]
    default: present
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage manage ntp servers
  stevefulme1.truenas.ntp:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    address: example_value
"""

RETURN = r"""
ntp:
  description: The manage ntp servers details.
  returned: success
  type: dict
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
        address=dict(type="str", required=True),
        burst=dict(type="bool", default=False),
        iburst=dict(type="bool", default=True),
        prefer=dict(type="bool", default=False),
        minpoll=dict(type="int", default=6),
        maxpoll=dict(type="int", default=10),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    state = module.params["state"]
    result = dict(changed=False)

    try:
        existing = None
        items = client.get("system/ntpserver")
        if isinstance(items, list):
            for item in items:
                if item.get("address") == module.params.get("address"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("system/ntpserver/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['address', 'burst', 'iburst', 'prefer', 'minpoll', 'maxpoll']:
                if module.params.get(key) is not None:
                    payload[key] = module.params[key]

            if existing:
                changes = {}
                for key, value in payload.items():
                    if existing.get(key) != value:
                        changes[key] = value
                if changes:
                    if not module.check_mode:
                        existing = client.put(
                            "system/ntpserver/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["ntp"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("system/ntpserver", payload)
                result["changed"] = True
                result["ntp"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
