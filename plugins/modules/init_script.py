#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: init_script
short_description: Manage init and shutdown scripts
version_added: "1.0.0"
description:
  - Manage init and shutdown scripts on a TrueNAS system via the middleware API.
options:
  type:
    description: Script type
    type: str
    default: COMMAND
    choices: ['COMMAND', 'SCRIPT']
  command:
    description: Command to run
    type: str
  script:
    description: Script path
    type: str
  when:
    description: When to run
    type: str
    required: true
    choices: ['PREINIT', 'POSTINIT', 'SHUTDOWN']
  comment:
    description: Script description
    type: str
  enabled:
    description: Enable the script
    type: bool
    default: True
  timeout:
    description: Timeout in seconds
    type: int
    default: 10
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
- name: Manage manage init and shutdown scripts
  stevefulme1.truenas.init_script:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    when: example_value
"""

RETURN = r"""
init_script:
  description: The manage init and shutdown scripts details.
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
        type=dict(type="str", default="COMMAND", choices=['COMMAND', 'SCRIPT']),
        command=dict(type="str"),
        script=dict(type="str"),
        when=dict(type="str", required=True, choices=['PREINIT', 'POSTINIT', 'SHUTDOWN']),
        comment=dict(type="str"),
        enabled=dict(type="bool", default=True),
        timeout=dict(type="int", default=10),
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
        items = client.get("initshutdownscript")
        if isinstance(items, list):
            for item in items:
                if item.get("comment") == module.params.get("comment"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("initshutdownscript/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['type', 'command', 'script', 'when', 'comment', 'enabled', 'timeout']:
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
                            "initshutdownscript/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["init_script"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("initshutdownscript", payload)
                result["changed"] = True
                result["init_script"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
