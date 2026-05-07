#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: pool
short_description: Manage ZFS storage pools
version_added: "1.0.0"
description:
  - Manage ZFS storage pools on a TrueNAS system via the middleware API.
options:
  name:
    description: Name of the storage pool
    type: str
    required: true
  topology:
    description: Pool topology definition with data, cache, log, spare, and special vdevs
    type: dict
  encryption:
    description: Enable encryption on the pool
    type: bool
    default: False
  encryption_algorithm:
    description: Encryption algorithm
    type: str
    default: AES-256-GCM
  deduplication:
    description: Deduplication setting
    type: str
    default: "OFF"
    choices: ['ON', 'OFF', 'VERIFY']
  checksum:
    description: Checksum algorithm
    type: str
    default: "ON"
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
- name: Manage manage zfs storage pools
  stevefulme1.storage.pool:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: example_value
"""

RETURN = r"""
pool:
  description: The manage zfs storage pools details.
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
        topology=dict(type="dict"),
        encryption=dict(type="bool", default=False),
        encryption_algorithm=dict(type="str", default="AES-256-GCM"),
        deduplication=dict(type="str", default="OFF", choices=['ON', 'OFF', 'VERIFY']),
        checksum=dict(type="str", default="ON"),
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
        items = client.get("pool")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("pool/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['name', 'topology', 'encryption', 'encryption_algorithm', 'deduplication', 'checksum']:
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
                            "pool/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["pool"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("pool", payload)
                result["changed"] = True
                result["pool"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
