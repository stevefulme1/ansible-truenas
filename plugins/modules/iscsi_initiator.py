#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: iscsi_initiator
short_description: Manage authorized iSCSI initiators
version_added: "1.0.0"
description:
  - Manage authorized iSCSI initiators on a TrueNAS system via the middleware API.
options:
  comment:
    description: Initiator group description
    type: str
  initiators:
    description: List of initiator IQNs (empty = allow all)
    type: list
    elements: str
  auth_network:
    description: Authorized networks (CIDR)
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
- name: Manage manage authorized iscsi initiators
  stevefulme1.storage.iscsi_initiator:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    state: present
"""

RETURN = r"""
iscsi_initiator:
  description: The manage authorized iscsi initiators details.
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
        comment=dict(type="str"),
        initiators=dict(type="list", elements="str"),
        auth_network=dict(type="list", elements="str"),
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
        items = client.get("iscsi/initiator")
        if isinstance(items, list):
            for item in items:
                if item.get("comment") == module.params.get("comment"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("iscsi/initiator/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['comment', 'initiators', 'auth_network']:
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
                            "iscsi/initiator/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["iscsi_initiator"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("iscsi/initiator", payload)
                result["changed"] = True
                result["iscsi_initiator"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
