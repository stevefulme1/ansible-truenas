#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ssh_connection
short_description: Manage SSH connections for replication
version_added: "1.0.0"
description:
  - Manage SSH connections for replication on a TrueNAS system via the middleware API.
options:
  name:
    description: Connection name
    type: str
    required: true
  host:
    description: Remote host
    type: str
    required: true
  port:
    description: SSH port
    type: int
    default: 22
  username:
    description: Remote username
    type: str
    default: root
  private_key:
    description: SSH private key content
    type: str
  remote_host_key:
    description: Remote host public key
    type: str
  state:
    description: Desired state of the resource.
    type: str
    choices: [present, absent]
    default: present
extends_documentation_fragment:
  - truenas.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage manage ssh connections for replication
  truenas.storage.ssh_connection:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: example_value
    host: example_value
"""

RETURN = r"""
ssh_connection:
  description: The manage ssh connections for replication details.
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
        name=dict(type="str", required=True),
        host=dict(type="str", required=True),
        port=dict(type="int", default=22),
        username=dict(type="str", default="root"),
        private_key=dict(type="str", no_log=True),
        remote_host_key=dict(type="str", no_log=False),
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
        items = client.get("keychaincredential")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("keychaincredential/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['name', 'host', 'port', 'username', 'private_key', 'remote_host_key']:
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
                            "keychaincredential/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["ssh_connection"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("keychaincredential", payload)
                result["changed"] = True
                _sensitive_keys = {'private_key'}
                safe_payload = {k: v for k, v in payload.items() if k not in _sensitive_keys}
                result["ssh_connection"] = existing or safe_payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
