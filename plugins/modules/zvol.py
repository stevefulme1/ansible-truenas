#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: zvol
short_description: Manage ZFS volumes (zvols)
version_added: "1.0.0"
description:
  - Manage ZFS volumes (zvols) on a TrueNAS system via the middleware API.
  - Create, update, or delete zvols for use with iSCSI targets or VM storage.
options:
  name:
    description: Full zvol path (pool/zvol_name)
    type: str
    required: true
  volsize:
    description: Volume size (e.g., 10G, 500M)
    type: str
  volblocksize:
    description: Volume block size (e.g., 4K, 8K, 16K, 32K, 64K, 128K)
    type: str
  sparse:
    description: Create a sparse (thin-provisioned) zvol
    type: bool
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
- name: Create a 10G zvol for iSCSI
  stevefulme1.truenas.zvol:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: tank/iscsi-vol1
    volsize: "10G"
    state: present

- name: Create a sparse zvol for VM storage
  stevefulme1.truenas.zvol:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: tank/vm-disk1
    volsize: "50G"
    sparse: true
    volblocksize: "16K"
    state: present

- name: Resize an existing zvol
  stevefulme1.truenas.zvol:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: tank/iscsi-vol1
    volsize: "20G"
    state: present

- name: Remove a zvol
  stevefulme1.truenas.zvol:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: tank/iscsi-vol1
    state: absent
"""

RETURN = r"""
zvol:
  description: The ZFS volume details.
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
        volsize=dict(type="str"),
        volblocksize=dict(type="str"),
        sparse=dict(type="bool"),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    name = module.params["name"]
    state = module.params["state"]
    result = dict(changed=False)
    encoded_name = quote(name, safe="")

    try:
        existing = None
        try:
            existing = client.get("pool/dataset/id/{0}".format(encoded_name))
        except TrueNASError:
            pass

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("pool/dataset/id/{0}".format(encoded_name))
                result["changed"] = True

        else:
            if module.params.get("volsize") is None and not existing:
                module.fail_json(msg="volsize is required when creating a new zvol")

            payload = {"type": "VOLUME", "name": name}
            for key in ["volsize", "volblocksize", "sparse"]:
                if module.params.get(key) is not None:
                    payload[key] = module.params[key]

            if existing:
                changes = {}
                if module.params.get("volsize") is not None and existing.get("volsize") != module.params["volsize"]:
                    changes["volsize"] = module.params["volsize"]
                if changes:
                    if not module.check_mode:
                        existing = client.put("pool/dataset/id/{0}".format(encoded_name), changes)
                    result["changed"] = True
                result["zvol"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("pool/dataset", payload)
                result["changed"] = True
                result["zvol"] = existing or payload

    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
