#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dataset
short_description: Manage ZFS datasets
version_added: "1.0.0"
description:
  - Manage ZFS datasets on a TrueNAS system via the middleware API.
options:
  name:
    description: Full dataset path (pool/dataset)
    type: str
    required: true
  type:
    description: Dataset type
    type: str
    default: FILESYSTEM
    choices: ['FILESYSTEM', 'VOLUME']
  quota:
    description: Quota (e.g., 100G)
    type: str
  refquota:
    description: Reference quota
    type: str
  reservation:
    description: Reservation
    type: str
  compression:
    description: Compression algorithm
    type: str
    default: LZ4
  recordsize:
    description: Record size (e.g., 128K)
    type: str
  atime:
    description: Access time tracking
    type: str
    choices: ['ON', 'OFF']
  sync:
    description: Sync write behavior
    type: str
    choices: ['STANDARD', 'ALWAYS', 'DISABLED']
  copies:
    description: Number of data copies
    type: int
    choices: [1, 2, 3]
  deduplication:
    description: Deduplication
    type: str
    choices: ['ON', 'OFF', 'VERIFY']
  encryption:
    description: Enable encryption
    type: bool
  volsize:
    description: Volume size for zvols
    type: str
  volblocksize:
    description: Volume block size for zvols
    type: str
  comments:
    description: Dataset comments
    type: str
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
- name: Create a dataset for media storage
  stevefulme1.truenas.dataset:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: tank/datasets/media
    compression: LZ4
    quota: 500G
    atime: "OFF"
    state: present

- name: Create an encrypted dataset for sensitive data
  stevefulme1.truenas.dataset:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: tank/datasets/secure
    encryption: true
    compression: ZSTD
    copies: 2
    comments: Encrypted storage for confidential files
    state: present

- name: Remove a dataset
  stevefulme1.truenas.dataset:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: tank/datasets/old-project
    state: absent
"""

RETURN = r"""
dataset:
  description: The manage zfs datasets details.
  returned: success
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.parse import quote
from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
    TrueNASClient,
    TrueNASError,
    truenas_argument_spec,
)


def main():
    argument_spec = truenas_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=True),
        type=dict(type="str", default="FILESYSTEM", choices=['FILESYSTEM', 'VOLUME']),
        quota=dict(type="str"),
        refquota=dict(type="str"),
        reservation=dict(type="str"),
        compression=dict(type="str", default="LZ4"),
        recordsize=dict(type="str"),
        atime=dict(type="str", choices=['ON', 'OFF']),
        sync=dict(type="str", choices=['STANDARD', 'ALWAYS', 'DISABLED']),
        copies=dict(type="int", choices=[1, 2, 3]),
        deduplication=dict(type="str", choices=['ON', 'OFF', 'VERIFY']),
        encryption=dict(type="bool"),
        volsize=dict(type="str"),
        volblocksize=dict(type="str"),
        comments=dict(type="str"),
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
        items = client.get("pool/dataset")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("pool/dataset/id/{0}".format(quote(str(existing["id"]), safe="")))
                result["changed"] = True
        else:
            payload = {}
            _fields = [
                'name', 'type', 'quota', 'refquota', 'reservation', 'compression', 'recordsize', 'atime', 'sync', 'copies', 'deduplication', 'encryption',
                'volsize', 'volblocksize', 'comments',
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
                            "pool/dataset/id/{0}".format(quote(str(existing["id"]), safe="")), changes
                        )
                    result["changed"] = True
                result["dataset"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("pool/dataset", payload)
                result["changed"] = True
                result["dataset"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
