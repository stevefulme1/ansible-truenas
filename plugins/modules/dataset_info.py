#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dataset_info
short_description: Gather ZFS dataset information
version_added: "1.1.0"
description:
  - Retrieve ZFS dataset information from a TrueNAS system via the middleware API.
options:
  name:
    description: Dataset name to query. Slashes are URL-encoded automatically.
    type: str
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: List all datasets
  stevefulme1.truenas.dataset_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"

- name: Get a specific dataset
  stevefulme1.truenas.dataset_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: tank/data
"""

RETURN = r"""
datasets:
  description: List of datasets.
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
        name=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    name = module.params.get("name")

    try:
        if name:
            encoded = name.replace("/", "%2F")
            data = client.get("pool/dataset/id/{0}".format(encoded))
            datasets = [data] if data else []
        else:
            data = client.get("pool/dataset")
            datasets = data if isinstance(data, list) else [data]

        module.exit_json(changed=False, datasets=datasets)
    except TrueNASError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
