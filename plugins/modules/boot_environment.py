#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: boot_environment
short_description: Manage boot environments
version_added: "1.0.0"
description:
  - Manage boot environments on a TrueNAS system via the middleware API.
  - Create, activate, or delete boot environments.
  - Supports cloning from an existing boot environment.
options:
  name:
    description: Name of the boot environment
    type: str
    required: true
  source:
    description: Name of an existing boot environment to clone from
    type: str
  state:
    description: Desired state of the boot environment.
    type: str
    choices: [present, absent, activated]
    default: present
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Create a boot environment
  stevefulme1.truenas.boot_environment:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: pre-upgrade-snapshot
    state: present

- name: Clone a boot environment
  stevefulme1.truenas.boot_environment:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: pre-upgrade-clone
    source: default
    state: present

- name: Activate a boot environment
  stevefulme1.truenas.boot_environment:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: pre-upgrade-snapshot
    state: activated

- name: Delete a boot environment
  stevefulme1.truenas.boot_environment:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    name: old-snapshot
    state: absent
"""

RETURN = r"""
boot_environment:
  description: The boot environment details.
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
        source=dict(type="str"),
        state=dict(type="str", choices=["present", "absent", "activated"], default="present"),
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
        items = client.get("bootenv")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == name:
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("bootenv/id/{0}".format(existing["id"]))
                result["changed"] = True

        elif state == "activated":
            if not existing:
                module.fail_json(msg="Boot environment '{0}' does not exist".format(name))
            if not existing.get("activated"):
                if not module.check_mode:
                    client.post("bootenv/id/{0}/activate".format(existing["id"]), {})
                result["changed"] = True
            result["boot_environment"] = existing

        else:
            if not existing:
                payload = {"name": name}
                if module.params.get("source"):
                    payload["source"] = module.params["source"]
                if not module.check_mode:
                    existing = client.post("bootenv", payload)
                result["changed"] = True
            result["boot_environment"] = existing or {"name": name}

    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
