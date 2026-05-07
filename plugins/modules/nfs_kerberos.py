#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: nfs_kerberos
short_description: Manage Kerberos principals for NFS
version_added: "1.0.0"
description:
  - Manage Kerberos principals for NFS on a TrueNAS system via the middleware API.
options:
  name:
    description: Keytab name
    type: str
    required: true
  file:
    description: Base64-encoded keytab file content
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
- name: Manage manage kerberos principals for nfs
  truenas.storage.nfs_kerberos:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: example_value
"""

RETURN = r"""
nfs_kerberos:
  description: The manage kerberos principals for nfs details.
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
        file=dict(type="str"),
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
        items = client.get("kerberos/keytab")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("kerberos/keytab/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['name', 'file']:
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
                            "kerberos/keytab/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["nfs_kerberos"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("kerberos/keytab", payload)
                result["changed"] = True
                result["nfs_kerberos"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
