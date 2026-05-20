#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: alert_service_info
short_description: Gather alert service configurations
version_added: "1.0.0"
description:
  - Gather alert service configurations from a TrueNAS system via the middleware API.
  - This is a read-only module.
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Get alert service configurations
  stevefulme1.truenas.alert_service_info:
    api_url: "https://truenas.example.com"
    api_key: "{ truenas_api_key }"
  register: result
"""

RETURN = r"""
alert_services:
  description: The alert service configurations.
  returned: success
  type: list
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
    TrueNASClient,
    TrueNASError,
    truenas_argument_spec,
)


def main():
    argument_spec = truenas_argument_spec()

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        data = client.get("alertservice")
        result["alert_services"] = data
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
