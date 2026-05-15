#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: enclosure_info
short_description: Get enclosure and disk shelf information
version_added: "1.3.0"
description:
  - Retrieve enclosure and disk shelf information from a TrueNAS system
    via the middleware API.
  - Returns a list of enclosures with model, controller, status, and
    element details (disks, PSUs, fans).
options:
  {}
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: List enclosures
  stevefulme1.truenas.enclosure_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
  register: enclosures

- name: Show enclosure details
  ansible.builtin.debug:
    var: enclosures.data
"""

RETURN = r"""
data:
  description: List of enclosure objects.
  returned: success
  type: list
  elements: dict
  contains:
    model:
      description: Enclosure model string.
      type: str
    controller:
      description: Whether this enclosure is a controller.
      type: bool
    status:
      description: Overall enclosure status list.
      type: list
    elements:
      description: >-
        Dict of element categories (Disk, Power Supply, Cooling)
        mapping to individual element status entries.
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
        data = client.get("enclosure")
        module.exit_json(changed=False, data=data)
    except TrueNASError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
