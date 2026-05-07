#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: snapshot_clone
short_description: Clone a ZFS snapshot into a new dataset
version_added: "1.0.0"
description:
  - Clone a ZFS snapshot into a new dataset on a TrueNAS system via the middleware API.
options:
  snapshot:
    description: Snapshot to clone (dataset@name)
    type: str
    required: true
  target:
    description: Target dataset name for the clone
    type: str
    required: true
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage clone a zfs snapshot into a new dataset
  stevefulme1.truenas.snapshot_clone:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    snapshot: example_value
    target: example_value
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
        snapshot=dict(type="str", required=True),
        target=dict(type="str", required=True),
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
            response = client.post("zfs/snapshot", {"snapshot": module.params["snapshot"], "target": module.params["target"]})
            result["result"] = response
        result["changed"] = True
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
