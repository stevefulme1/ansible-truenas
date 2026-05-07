#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dataset_promote
short_description: Promote a ZFS clone to an independent dataset
version_added: "1.0.0"
description:
  - Promote a ZFS clone to an independent dataset on a TrueNAS system via the middleware API.
options:
  name:
    description: Clone dataset to promote
    type: str
    required: true
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Promote a ZFS clone to an independent dataset
  stevefulme1.truenas.dataset_promote:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: tank/datasets/media-clone

- name: Promote a restored clone as the new primary dataset
  stevefulme1.truenas.dataset_promote:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: tank/datasets/db-restored
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
        name=dict(type="str", required=True),
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
            response = client.post("pool/dataset", {"name": module.params["name"]})
            result["result"] = response
        result["changed"] = True
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
