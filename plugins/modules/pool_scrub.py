#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: pool_scrub
short_description: Configure pool scrub schedules
version_added: "1.0.0"
description:
  - Configure pool scrub schedules on a TrueNAS system via the middleware API.
options:
  pool:
    description: Pool to scrub
    type: str
    required: true
  threshold:
    description: Days between scrubs threshold
    type: int
    default: 35
  schedule:
    description: Cron schedule for scrub
    type: dict
  enabled:
    description: Enable the scrub task
    type: bool
    default: True
  state:
    description: Desired state of the resource.
    type: str
    choices: [present, absent]
    default: present
extends_documentation_fragment:
  - truenas.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure pool scrub schedules
  truenas.storage.pool_scrub:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    pool: example_value
"""

RETURN = r"""
pool_scrub:
  description: The configure pool scrub schedules details.
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
        pool=dict(type="str", required=True),
        threshold=dict(type="int", default=35),
        schedule=dict(type="dict"),
        enabled=dict(type="bool", default=True),
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
        items = client.get("pool/scrub")
        if isinstance(items, list):
            for item in items:
                if item.get("pool_name") == module.params.get("pool_name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("pool/scrub/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['pool', 'threshold', 'schedule', 'enabled']:
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
                            "pool/scrub/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["pool_scrub"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("pool/scrub", payload)
                result["changed"] = True
                result["pool_scrub"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
