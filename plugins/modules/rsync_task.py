#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rsync_task
short_description: Configure rsync tasks
version_added: "1.0.0"
description:
  - Configure rsync tasks on a TrueNAS system via the middleware API.
options:
  path:
    description: Local path
    type: str
    required: true
  remotehost:
    description: Remote host
    type: str
    required: true
  remotemodule:
    description: Remote rsync module
    type: str
  remotepath:
    description: Remote path
    type: str
  direction:
    description: Sync direction
    type: str
    default: PUSH
    choices: ['PUSH', 'PULL']
  schedule:
    description: Cron schedule
    type: dict
  recursive:
    description: Recursive sync
    type: bool
    default: True
  compress:
    description: Enable compression
    type: bool
    default: True
  archive:
    description: Archive mode
    type: bool
    default: True
  delete:
    description: Delete files on destination
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
  - truenas.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure rsync tasks
  truenas.storage.rsync_task:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    path: example_value
    remotehost: example_value
"""

RETURN = r"""
rsync_task:
  description: The configure rsync tasks details.
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
        path=dict(type="str", required=True),
        remotehost=dict(type="str", required=True),
        remotemodule=dict(type="str"),
        remotepath=dict(type="str"),
        direction=dict(type="str", default="PUSH", choices=['PUSH', 'PULL']),
        schedule=dict(type="dict"),
        recursive=dict(type="bool", default=True),
        compress=dict(type="bool", default=True),
        archive=dict(type="bool", default=True),
        delete=dict(type="bool", default=False),
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
        items = client.get("rsynctask")
        if isinstance(items, list):
            for item in items:
                if item.get("path") == module.params.get("path"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("rsynctask/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['path', 'remotehost', 'remotemodule', 'remotepath', 'direction', 'schedule', 'recursive', 'compress', 'archive', 'delete', 'enabled']:
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
                            "rsynctask/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["rsync_task"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("rsynctask", payload)
                result["changed"] = True
                result["rsync_task"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
