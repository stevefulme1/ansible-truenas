#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: update_info
short_description: Get available system updates
version_added: "1.3.0"
description:
  - Check for available system updates on a TrueNAS system via the
    middleware API.
  - Returns whether updates are available, the target version,
    changelog, and a list of individual changes.
options:
  {}
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Check for available updates
  stevefulme1.truenas.update_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
  register: updates

- name: Show update status
  ansible.builtin.debug:
    msg: >-
      Updates available: {{ updates.available }},
      version: {{ updates.version | default('N/A') }}
"""

RETURN = r"""
available:
  description: Whether updates are available.
  returned: success
  type: bool
version:
  description: Target update version string.
  returned: when updates are available
  type: str
changelog:
  description: Release notes / changelog text.
  returned: when updates are available
  type: str
changes:
  description: List of individual changes included in the update.
  returned: when updates are available
  type: list
  elements: dict
data:
  description: Full response from the update check API.
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

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)

    try:
        data = client.post("update/check_available")
        available = bool(data.get("status") == "AVAILABLE")
        result = dict(
            changed=False,
            available=available,
            data=data,
        )
        if available:
            result["version"] = data.get("version", "")
            result["changelog"] = data.get("changelog", "")
            result["changes"] = data.get("changes", [])
        module.exit_json(**result)
    except TrueNASError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
