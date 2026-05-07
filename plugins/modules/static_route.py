#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: static_route
short_description: Manage static routes
version_added: "1.0.0"
description:
  - Manage static routes on a TrueNAS system via the middleware API.
options:
  destination:
    description: Destination network (CIDR)
    type: str
    required: true
  gateway:
    description: Gateway address
    type: str
    required: true
  description:
    description: Route description
    type: str
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
- name: Manage manage static routes
  stevefulme1.storage.static_route:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    destination: example_value
    gateway: example_value
"""

RETURN = r"""
static_route:
  description: The manage static routes details.
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
        destination=dict(type="str", required=True),
        gateway=dict(type="str", required=True),
        description=dict(type="str"),
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
        items = client.get("staticroute")
        if isinstance(items, list):
            for item in items:
                if item.get("destination") == module.params.get("destination"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("staticroute/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['destination', 'gateway', 'description']:
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
                            "staticroute/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["static_route"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("staticroute", payload)
                result["changed"] = True
                result["static_route"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
