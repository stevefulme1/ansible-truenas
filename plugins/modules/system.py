#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: system
short_description: Configure general system settings
version_added: "1.0.0"
description:
  - Configure general system settings on a TrueNAS system via the middleware API.
options:
  hostname:
    description: System hostname
    type: str
  timezone:
    description: System timezone
    type: str
  language:
    description: UI language
    type: str
    default: en
  crash_reporting:
    description: Enable crash reporting
    type: bool
  usage_collection:
    description: Enable usage statistics
    type: bool
extends_documentation_fragment:
  - truenas.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure general system settings
  truenas.storage.system:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    state: present
"""

RETURN = r"""
config:
  description: Current configuration.
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
        hostname=dict(type="str"),
        timezone=dict(type="str"),
        language=dict(type="str", default="en"),
        crash_reporting=dict(type="bool"),
        usage_collection=dict(type="bool"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        current = client.get("system/general")
        payload = {}
        if module.params["hostname"] is not None and current.get("hostname") != module.params["hostname"]:
            payload["hostname"] = module.params["hostname"]
        if module.params["timezone"] is not None and current.get("timezone") != module.params["timezone"]:
            payload["timezone"] = module.params["timezone"]
        if module.params["language"] is not None and current.get("language") != module.params["language"]:
            payload["language"] = module.params["language"]
        if module.params["crash_reporting"] is not None and current.get("crash_reporting") != module.params["crash_reporting"]:
            payload["crash_reporting"] = module.params["crash_reporting"]
        if module.params["usage_collection"] is not None and current.get("usage_collection") != module.params["usage_collection"]:
            payload["usage_collection"] = module.params["usage_collection"]
        if payload:
            if not module.check_mode:
                current = client.put("system/general", payload)
            result["changed"] = True
        result["config"] = current
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
