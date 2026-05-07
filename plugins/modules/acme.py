#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: acme
short_description: Configure ACME (Let's Encrypt) registration
version_added: "1.0.0"
description:
  - Configure ACME (Let's Encrypt) registration on a TrueNAS system via the middleware API.
options:
  name:
    description: Registration name
    type: str
    required: true
  tos:
    description: Accept terms of service
    type: bool
    default: True
  email:
    description: Contact email
    type: str
    required: true
  directory_uri:
    description: ACME directory URI
    type: str
    default: https://acme-v02.api.letsencrypt.org/directory
  state:
    description: Desired state of the resource.
    type: str
    choices: [present, absent]
    default: present
extends_documentation_fragment:
  - stevefulme1.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure acme (let's encrypt) registration
  stevefulme1.storage.acme:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: example_value
    email: example_value
"""

RETURN = r"""
acme:
  description: The configure acme (let's encrypt) registration details.
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
        name=dict(type="str", required=True),
        tos=dict(type="bool", default=True),
        email=dict(type="str", required=True),
        directory_uri=dict(type="str", default="https://acme-v02.api.letsencrypt.org/directory"),
        state=dict(type="str", choices=["present", "absent"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    state = module.params["state"]
    result = dict(changed=False)

    try:
        existing = None
        items = client.get("acme/registration")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("acme/registration/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['name', 'tos', 'email', 'directory_uri']:
                if module.params.get(key) is not None:
                    payload[key] = module.params[key]

            if existing:
                changes = {}
                for key, value in payload.items():
                    if existing.get(key) != value:
                        changes[key] = value
                if changes:
                    if not module.check_mode:
                        existing = client.put(
                            "acme/registration/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["acme"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("acme/registration", payload)
                result["changed"] = True
                result["acme"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
