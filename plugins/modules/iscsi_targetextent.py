#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: iscsi_targetextent
short_description: Associate iSCSI targets with extents
version_added: "1.0.0"
description:
  - Associate iSCSI targets with extents on a TrueNAS system via the middleware API.
options:
  target:
    description: Target ID
    type: int
    required: true
  extent:
    description: Extent ID
    type: int
    required: true
  lunid:
    description: LUN ID (auto-assigned if omitted)
    type: int
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
- name: Manage associate iscsi targets with extents
  truenas.storage.iscsi_targetextent:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    target: 1
    extent: 1
"""

RETURN = r"""
iscsi_targetextent:
  description: The associate iscsi targets with extents details.
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
        target=dict(type="int", required=True),
        extent=dict(type="int", required=True),
        lunid=dict(type="int"),
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
        items = client.get("iscsi/targetextent")
        if isinstance(items, list):
            for item in items:
                if item.get("None") == module.params.get("None"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("iscsi/targetextent/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['target', 'extent', 'lunid']:
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
                            "iscsi/targetextent/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["iscsi_targetextent"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("iscsi/targetextent", payload)
                result["changed"] = True
                result["iscsi_targetextent"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
