#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: snapshot_info
short_description: Gather ZFS snapshot information
version_added: "1.1.0"
description:
  - Retrieve ZFS snapshot information from a TrueNAS system via the middleware API.
options:
  dataset:
    description: Dataset name to filter snapshots by.
    type: str
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: List all snapshots
  stevefulme1.truenas.snapshot_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"

- name: List snapshots for a dataset
  stevefulme1.truenas.snapshot_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    dataset: tank/data
"""

RETURN = r"""
snapshots:
  description: List of ZFS snapshots.
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
        dataset=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    dataset = module.params.get("dataset")

    try:
        data = client.get("zfs/snapshot")
        snapshots = data if isinstance(data, list) else [data]

        if dataset:
            snapshots = [s for s in snapshots if s.get("dataset") == dataset]

        module.exit_json(changed=False, snapshots=snapshots)
    except TrueNASError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
