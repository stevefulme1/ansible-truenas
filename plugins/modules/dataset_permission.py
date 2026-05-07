#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dataset_permission
short_description: Set POSIX or NFSv4 ACL permissions on a dataset
version_added: "1.0.0"
description:
  - Set POSIX or NFSv4 ACL permissions on a dataset on a TrueNAS system via the middleware API.
options:
  path:
    description: Filesystem path
    type: str
    required: true
  owner:
    description: Owner user
    type: str
  group:
    description: Owner group
    type: str
  mode:
    description: POSIX mode (e.g., 0755)
    type: str
  acl_type:
    description: ACL type
    type: str
    choices: ['POSIX', 'NFS4']
  acl_entries:
    description: List of ACL entries
    type: list
    elements: str
  recursive:
    description: Apply recursively
    type: bool
    default: False
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage set posix or nfsv4 acl permissions on a dataset
  stevefulme1.truenas.dataset_permission:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    path: example_value
"""

RETURN = r"""
result:
  description: Action result.
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
        path=dict(type="str", required=True),
        owner=dict(type="str"),
        group=dict(type="str"),
        mode=dict(type="str"),
        acl_type=dict(type="str", choices=['POSIX', 'NFS4']),
        acl_entries=dict(type="list", elements="str"),
        recursive=dict(type="bool", default=False),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        if not module.check_mode:
            response = client.post("pool/dataset", {
                "path": module.params["path"],
                "owner": module.params["owner"],
                "group": module.params["group"],
                "mode": module.params["mode"],
                "acl_type": module.params["acl_type"],
                "acl_entries": module.params["acl_entries"],
                "recursive": module.params["recursive"],
            })
            result["result"] = response
        result["changed"] = True
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
