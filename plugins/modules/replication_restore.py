#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: replication_restore
short_description: Restore from a replication target
version_added: "1.0.0"
description:
  - Restore from a replication target on a TrueNAS system via the middleware API.
options:
  task_id:
    description: Replication task ID
    type: int
    required: true
  target_dataset:
    description: Dataset to restore into
    type: str
    required: true
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage restore from a replication target
  stevefulme1.truenas.replication_restore:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    task_id: 1
    target_dataset: example_value
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
        task_id=dict(type="int", required=True),
        target_dataset=dict(type="str", required=True),
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
            response = client.post("replication/restore", {"task_id": module.params["task_id"], "target_dataset": module.params["target_dataset"]})
            result["result"] = response
        result["changed"] = True
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
