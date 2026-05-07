#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dataset_unlock
short_description: Unlock an encrypted dataset
version_added: "1.0.0"
description:
  - Unlock an encrypted dataset on a TrueNAS system via the middleware API.
options:
  name:
    description: Dataset name
    type: str
    required: true
  passphrase:
    description: Encryption passphrase
    type: str
  key_file:
    description: Path to encryption key file
    type: str
  recursive:
    description: Unlock child datasets
    type: bool
    default: False
extends_documentation_fragment:
  - truenas.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage unlock an encrypted dataset
  truenas.storage.dataset_unlock:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: example_value
"""

RETURN = r"""
result:
  description: Action result.
  returned: success
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.truenas.storage.plugins.module_utils.truenas_api import (
    TrueNASClient,
    TrueNASError,
    truenas_argument_spec,
)


def main():
    argument_spec = truenas_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=True),
        passphrase=dict(type="str", no_log=True),
        key_file=dict(type="str"),
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
                "name": module.params["name"],
                "passphrase": module.params["passphrase"],
                "key_file": module.params["key_file"],
                "recursive": module.params["recursive"],
            })
            result["result"] = response
        result["changed"] = True
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
