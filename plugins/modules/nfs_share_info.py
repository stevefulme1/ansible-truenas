#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: nfs_share_info
short_description: Gather NFS export information
version_added: "1.1.0"
description:
  - Retrieve NFS export configuration from a TrueNAS system via the middleware API.
options:
  id:
    description: NFS export ID to filter results.
    type: int
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: List all NFS exports
  stevefulme1.truenas.nfs_share_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"

- name: Get a specific NFS export
  stevefulme1.truenas.nfs_share_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    id: 1
"""

RETURN = r"""
exports:
  description: List of NFS exports.
  returned: success
  type: list
  elements: dict
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
        id=dict(type="int"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    nfs_id = module.params.get("id")

    try:
        data = client.get("sharing/nfs")
        exports = data if isinstance(data, list) else [data]

        if nfs_id is not None:
            exports = [e for e in exports if e.get("id") == nfs_id]

        module.exit_json(changed=False, exports=exports)
    except TrueNASError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
