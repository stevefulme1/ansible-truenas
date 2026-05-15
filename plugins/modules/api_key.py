#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: api_key
short_description: Manage API keys
version_added: "1.0.0"
description:
  - Manage API keys on a TrueNAS system via the middleware API.
  - Create or delete API keys for programmatic access.
  - The created key value is returned only on creation and marked as sensitive.
options:
  name:
    description: Name of the API key
    type: str
    required: true
  state:
    description: Desired state of the resource.
    type: str
    choices: [present, absent]
    default: present
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Create an API key
  stevefulme1.truenas.api_key:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: automation-key
    state: present
  register: new_key
  no_log: true

- name: Delete an API key
  stevefulme1.truenas.api_key:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: automation-key
    state: absent
"""

RETURN = r"""
api_key:
  description: The API key details. The key value is only returned on creation.
  returned: success
  type: dict
  contains:
    key:
      description: The API key value (only on creation).
      returned: when created
      type: str
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
        name=dict(type="str", required=True, no_log=False),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    name = module.params["name"]
    state = module.params["state"]
    result = dict(changed=False)

    try:
        existing = None
        items = client.get("api_key")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == name:
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("api_key/id/{0}".format(existing["id"]))
                result["changed"] = True

        else:
            if not existing:
                if not module.check_mode:
                    created = client.post("api_key", {"name": name})
                    result["api_key"] = created
                    module.no_log_values.add(created.get("key", ""))
                else:
                    result["api_key"] = {"name": name}
                result["changed"] = True
            else:
                result["api_key"] = existing

    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
