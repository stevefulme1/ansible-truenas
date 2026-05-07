#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cloud_sync
short_description: Configure cloud sync tasks
version_added: "1.0.0"
description:
  - Configure cloud sync tasks on a TrueNAS system via the middleware API.
options:
  description:
    description: Task description
    type: str
    required: true
  credential:
    description: Cloud credential ID
    type: int
    required: true
  direction:
    description: Sync direction
    type: str
    required: true
    choices: ['PUSH', 'PULL']
  transfer_mode:
    description: Transfer mode
    type: str
    default: SYNC
    choices: ['SYNC', 'COPY', 'MOVE']
  path:
    description: Local path
    type: str
    required: true
  bucket:
    description: Remote bucket name
    type: str
  folder:
    description: Remote folder path
    type: str
  schedule:
    description: Cron schedule
    type: dict
  encryption:
    description: Enable encryption
    type: bool
    default: False
  bandwidth_limit:
    description: Bandwidth limit rules
    type: list
    elements: str
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
- name: Create a cloud sync task to push backups to S3
  stevefulme1.truenas.cloud_sync:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    description: Daily backup to S3
    credential: 1
    direction: PUSH
    transfer_mode: SYNC
    path: /mnt/tank/backups
    bucket: truenas-backups
    folder: /daily
    schedule:
      minute: "0"
      hour: "2"
      dom: "*"
      month: "*"
      dow: "*"
    enabled: true
    state: present

- name: Create a cloud sync task to pull data from S3
  stevefulme1.truenas.cloud_sync:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    description: Pull shared assets from S3
    credential: 1
    direction: PULL
    transfer_mode: COPY
    path: /mnt/data/shared-assets
    bucket: company-assets
    folder: /media
    state: present

- name: Remove a cloud sync task
  stevefulme1.truenas.cloud_sync:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    description: Daily backup to S3
    state: absent
"""

RETURN = r"""
cloud_sync:
  description: The configure cloud sync tasks details.
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
        description=dict(type="str", required=True),
        credential=dict(type="int", required=True),
        direction=dict(type="str", required=True, choices=['PUSH', 'PULL']),
        transfer_mode=dict(type="str", default="SYNC", choices=['SYNC', 'COPY', 'MOVE']),
        path=dict(type="str", required=True),
        bucket=dict(type="str"),
        folder=dict(type="str"),
        schedule=dict(type="dict"),
        encryption=dict(type="bool", default=False),
        bandwidth_limit=dict(type="list", elements="str"),
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
        items = client.get("cloudsync")
        if isinstance(items, list):
            for item in items:
                if item.get("description") == module.params.get("description"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("cloudsync/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            _fields = [
                'description', 'credential', 'direction', 'transfer_mode', 'path', 'bucket', 'folder', 'schedule', 'encryption', 'bandwidth_limit',
                'enabled',
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
                            "cloudsync/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["cloud_sync"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("cloudsync", payload)
                result["changed"] = True
                result["cloud_sync"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
