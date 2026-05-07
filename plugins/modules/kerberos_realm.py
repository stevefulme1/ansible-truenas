#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: kerberos_realm
short_description: Manage Kerberos realms
version_added: "1.0.0"
description:
  - Manage Kerberos realms on a TrueNAS system via the middleware API.
options:
  realm:
    description: Kerberos realm name
    type: str
    required: true
  kdc:
    description: KDC servers
    type: list
    elements: str
  admin_server:
    description: Admin servers
    type: list
    elements: str
  kpasswd_server:
    description: Password change servers
    type: list
    elements: str
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
- name: Create a Kerberos realm
  stevefulme1.truenas.kerberos_realm:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    realm: CORP.EXAMPLE.COM
    kdc:
      - dc01.corp.example.com
      - dc02.corp.example.com
    admin_server:
      - dc01.corp.example.com
    state: present

- name: Remove a Kerberos realm
  stevefulme1.truenas.kerberos_realm:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    realm: OLD.EXAMPLE.COM
    state: absent
"""

RETURN = r"""
kerberos_realm:
  description: The manage kerberos realms details.
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
        realm=dict(type="str", required=True),
        kdc=dict(type="list", elements="str"),
        admin_server=dict(type="list", elements="str"),
        kpasswd_server=dict(type="list", elements="str", no_log=False),
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
        items = client.get("kerberos/realm")
        if isinstance(items, list):
            for item in items:
                if item.get("realm") == module.params.get("realm"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("kerberos/realm/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['realm', 'kdc', 'admin_server', 'kpasswd_server']:
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
                            "kerberos/realm/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["kerberos_realm"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("kerberos/realm", payload)
                result["changed"] = True
                result["kerberos_realm"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
