#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: iscsi_target_info
short_description: Gather iSCSI target information
version_added: "1.1.0"
description:
  - Retrieve iSCSI target configuration from a TrueNAS system via the middleware API.
options:
  name:
    description: Target name to filter results.
    type: str
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: List all iSCSI targets
  stevefulme1.truenas.iscsi_target_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"

- name: Get a specific iSCSI target
  stevefulme1.truenas.iscsi_target_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: iqn.2005-10.org.freenas.ctl:target0
"""

RETURN = r"""
targets:
  description: List of iSCSI targets.
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
        data = client.get("iscsi/target")
        targets = data if isinstance(data, list) else [data]

        if name:
            targets = [t for t in targets if t.get("name") == name]

        module.exit_json(changed=False, targets=targets)
    except TrueNASError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
