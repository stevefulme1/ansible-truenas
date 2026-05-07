#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: alert_policy
short_description: Configure alert class policies
version_added: "1.0.0"
description:
  - Configure alert class policies on a TrueNAS system via the middleware API.
options:
  classes:
    description: Dict of alert class to policy mapping
    type: dict
    required: true
extends_documentation_fragment:
  - stevefulme1.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure alert class policies
  stevefulme1.storage.alert_policy:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    classes: {}
"""

RETURN = r"""
config:
  description: Current configuration.
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
        classes=dict(type="dict", required=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        current = client.get("alertclasses")
        payload = {}
        if module.params["classes"] is not None and current.get("classes") != module.params["classes"]:
            payload["classes"] = module.params["classes"]
        if payload:
            if not module.check_mode:
                current = client.put("alertclasses", payload)
            result["changed"] = True
        result["config"] = current
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
