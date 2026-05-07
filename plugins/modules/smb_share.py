#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: smb_share
short_description: Manage SMB/CIFS shares
version_added: "1.0.0"
description:
  - Manage SMB/CIFS shares on a TrueNAS system via the middleware API.
options:
  name:
    description: Share name
    type: str
    required: true
  path:
    description: Filesystem path to share
    type: str
  comment:
    description: Share description
    type: str
  readonly:
    description: Read-only share
    type: bool
    default: False
  browsable:
    description: Visible in network browser
    type: bool
    default: True
  guestok:
    description: Allow guest access
    type: bool
    default: False
  recyclebin:
    description: Enable recycle bin
    type: bool
    default: False
  shadowcopy:
    description: Enable shadow copies from snapshots
    type: bool
    default: True
  audit_logging:
    description: Enable audit logging
    type: bool
    default: False
  hostsallow:
    description: Allowed hosts
    type: list
    elements: str
  hostsdeny:
    description: Denied hosts
    type: list
    elements: str
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
- name: Manage manage smb/cifs shares
  stevefulme1.storage.smb_share:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: example_value
"""

RETURN = r"""
smb_share:
  description: The manage smb/cifs shares details.
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
        name=dict(type="str", required=True),
        path=dict(type="str"),
        comment=dict(type="str"),
        readonly=dict(type="bool", default=False),
        browsable=dict(type="bool", default=True),
        guestok=dict(type="bool", default=False),
        recyclebin=dict(type="bool", default=False),
        shadowcopy=dict(type="bool", default=True),
        audit_logging=dict(type="bool", default=False),
        hostsallow=dict(type="list", elements="str"),
        hostsdeny=dict(type="list", elements="str"),
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
        items = client.get("sharing/smb")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("sharing/smb/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['name', 'path', 'comment', 'readonly', 'browsable', 'guestok', 'recyclebin', 'shadowcopy', 'audit_logging', 'hostsallow', 'hostsdeny']:
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
                            "sharing/smb/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["smb_share"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("sharing/smb", payload)
                result["changed"] = True
                result["smb_share"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
