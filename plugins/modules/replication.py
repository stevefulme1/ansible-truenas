#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: replication
short_description: Configure ZFS replication tasks
version_added: "1.0.0"
description:
  - Configure ZFS replication tasks on a TrueNAS system via the middleware API.
options:
  name:
    description: Replication task name
    type: str
    required: true
  source_datasets:
    description: Source datasets to replicate
    type: list
    elements: str
    required: true
  target_dataset:
    description: Target dataset path
    type: str
    required: true
  direction:
    description: Replication direction
    type: str
    default: PUSH
    choices: ['PUSH', 'PULL']
  transport:
    description: Transport method
    type: str
    default: SSH
    choices: ['SSH', 'LOCAL']
  ssh_credentials:
    description: SSH credential ID for remote replication
    type: int
  schedule:
    description: Cron schedule
    type: dict
  recursive:
    description: Replicate child datasets
    type: bool
    default: True
  retention_policy:
    description: Snapshot retention policy
    type: str
    default: SOURCE
    choices: ['SOURCE', 'CUSTOM', 'NONE']
  retention_count:
    description: Number of snapshots to retain
    type: int
  speed_limit:
    description: Speed limit in bytes/sec (0 for unlimited)
    type: int
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
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Create a local replication task
  stevefulme1.truenas.replication:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: local-backup
    source_datasets:
      - tank/datasets/media
      - tank/datasets/documents
    target_dataset: backup/replicated
    transport: LOCAL
    recursive: true
    retention_policy: SOURCE
    schedule:
      minute: "0"
      hour: "1"
      dom: "*"
      month: "*"
      dow: "*"
    state: present

- name: Create a remote SSH replication task
  stevefulme1.truenas.replication:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: offsite-replication
    source_datasets:
      - tank/datasets/critical
    target_dataset: backup/offsite
    direction: PUSH
    transport: SSH
    ssh_credentials: 1
    recursive: true
    speed_limit: 10485760
    enabled: true
    state: present

- name: Remove a replication task
  stevefulme1.truenas.replication:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: old-replication
    state: absent
"""

RETURN = r"""
replication:
  description: The configure zfs replication tasks details.
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
        name=dict(type="str", required=True),
        source_datasets=dict(type="list", elements="str", required=True),
        target_dataset=dict(type="str", required=True),
        direction=dict(type="str", default="PUSH", choices=['PUSH', 'PULL']),
        transport=dict(type="str", default="SSH", choices=['SSH', 'LOCAL']),
        ssh_credentials=dict(type="int"),
        schedule=dict(type="dict"),
        recursive=dict(type="bool", default=True),
        retention_policy=dict(type="str", default="SOURCE", choices=['SOURCE', 'CUSTOM', 'NONE']),
        retention_count=dict(type="int"),
        speed_limit=dict(type="int"),
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
        items = client.get("replication")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("replication/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            _fields = [
                'name', 'source_datasets', 'target_dataset', 'direction', 'transport', 'ssh_credentials', 'schedule', 'recursive', 'retention_policy',
                'retention_count', 'speed_limit', 'enabled',
            ]
            for key in _fields:
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
                            "replication/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["replication"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("replication", payload)
                result["changed"] = True
                result["replication"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
