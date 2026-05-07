#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: iscsi_extent
short_description: Manage iSCSI extents (LUNs)
version_added: "1.0.0"
description:
  - Manage iSCSI extents (LUNs) on a TrueNAS system via the middleware API.
options:
  name:
    description: Extent name
    type: str
    required: true
  type:
    description: Extent type
    type: str
    default: DISK
    choices: ['DISK', 'FILE']
  disk:
    description: Zvol path for DISK type
    type: str
  path:
    description: File path for FILE type
    type: str
  filesize:
    description: File size for FILE type
    type: str
  blocksize:
    description: Logical block size
    type: int
    default: 512
  rpm:
    description: Reported RPM
    type: str
    default: SSD
    choices: ['UNKNOWN', 'SSD', '5400', '7200', '10000', '15000']
  readonly:
    description: Read-only extent
    type: bool
    default: False
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
- name: Manage manage iscsi extents (luns)
  truenas.storage.iscsi_extent:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: example_value
"""

RETURN = r"""
iscsi_extent:
  description: The manage iscsi extents (luns) details.
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
        name=dict(type="str", required=True),
        type=dict(type="str", default="DISK", choices=['DISK', 'FILE']),
        disk=dict(type="str"),
        path=dict(type="str"),
        filesize=dict(type="str"),
        blocksize=dict(type="int", default=512),
        rpm=dict(type="str", default="SSD", choices=['UNKNOWN', 'SSD', '5400', '7200', '10000', '15000']),
        readonly=dict(type="bool", default=False),
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
        items = client.get("iscsi/extent")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("iscsi/extent/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['name', 'type', 'disk', 'path', 'filesize', 'blocksize', 'rpm', 'readonly']:
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
                            "iscsi/extent/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["iscsi_extent"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("iscsi/extent", payload)
                result["changed"] = True
                result["iscsi_extent"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
