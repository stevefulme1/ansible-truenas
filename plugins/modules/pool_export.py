#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: pool_export
short_description: Export or import a ZFS pool
version_added: "1.0.0"
description:
  - Export or import a ZFS pool on a TrueNAS system via the middleware API.
options:
  pool:
    description: Pool name
    type: str
    required: true
  action:
    description: Action to perform
    type: str
    required: true
    choices: ['export', 'import']
  cascade:
    description: Destroy shares and services using this pool on export
    type: bool
    default: False
extends_documentation_fragment:
  - stevefulme1.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage export or import a zfs pool
  stevefulme1.storage.pool_export:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    pool: example_value
    action: example_value
"""

RETURN = r"""
result:
  description: Action result.
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
        pool=dict(type="str", required=True),
        action=dict(type="str", required=True, choices=['export', 'import']),
        cascade=dict(type="bool", default=False),
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
            response = client.post("pool", {"pool": module.params["pool"], "action": module.params["action"], "cascade": module.params["cascade"]})
            result["result"] = response
        result["changed"] = True
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
