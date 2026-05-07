#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: snapshot_task
short_description: Configure periodic snapshot tasks
version_added: "1.0.0"
description:
  - Configure periodic snapshot tasks on a TrueNAS system via the middleware API.
options:
  dataset:
    description: Dataset for snapshots
    type: str
    required: true
  schedule:
    description: Cron schedule
    type: dict
  lifetime_value:
    description: Snapshot retention value
    type: int
    default: 14
  lifetime_unit:
    description: Retention unit
    type: str
    default: DAY
    choices: ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']
  naming_schema:
    description: Snapshot naming schema
    type: str
    default: auto-%Y-%m-%d_%H-%M
  recursive:
    description: Create recursive snapshots
    type: bool
    default: False
  enabled:
    description: Enable the task
    type: bool
    default: True
  state:
    description: Desired state of the resource.
    type: str
    choices: [present, absent]
    default: present
extends_documentation_fragment:
  - stevefulme1.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure periodic snapshot tasks
  stevefulme1.storage.snapshot_task:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    dataset: example_value
"""

RETURN = r"""
snapshot_task:
  description: The configure periodic snapshot tasks details.
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
        dataset=dict(type="str", required=True),
        schedule=dict(type="dict"),
        lifetime_value=dict(type="int", default=14),
        lifetime_unit=dict(type="str", default="DAY", choices=['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']),
        naming_schema=dict(type="str", default="auto-%Y-%m-%d_%H-%M"),
        recursive=dict(type="bool", default=False),
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
        items = client.get("pool/snapshottask")
        if isinstance(items, list):
            for item in items:
                if item.get("dataset") == module.params.get("dataset"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("pool/snapshottask/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['dataset', 'schedule', 'lifetime_value', 'lifetime_unit', 'naming_schema', 'recursive', 'enabled']:
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
                            "pool/snapshottask/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["snapshot_task"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("pool/snapshottask", payload)
                result["changed"] = True
                result["snapshot_task"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
