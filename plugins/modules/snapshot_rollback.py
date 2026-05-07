#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: snapshot_rollback
short_description: Rollback a dataset to a specific snapshot
version_added: "1.0.0"
description:
  - Rollback a dataset to a specific snapshot on a TrueNAS system via the middleware API.
options:
  dataset:
    description: Dataset to rollback
    type: str
    required: true
  snapshot:
    description: Snapshot name to rollback to
    type: str
    required: true
  recursive:
    description: Include child datasets
    type: bool
    default: False
  force:
    description: Force rollback destroying newer snapshots
    type: bool
    default: False
extends_documentation_fragment:
  - stevefulme1.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage rollback a dataset to a specific snapshot
  stevefulme1.storage.snapshot_rollback:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    dataset: example_value
    snapshot: example_value
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
        dataset=dict(type="str", required=True),
        snapshot=dict(type="str", required=True),
        recursive=dict(type="bool", default=False),
        force=dict(type="bool", default=False),
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
            response = client.post("zfs/snapshot", {
                "dataset": module.params["dataset"],
                "snapshot": module.params["snapshot"],
                "recursive": module.params["recursive"],
                "force": module.params["force"],
            })
            result["result"] = response
        result["changed"] = True
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
