#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cloud_credential
short_description: Manage cloud storage credentials
version_added: "1.0.0"
description:
  - Manage cloud storage credentials on a TrueNAS system via the middleware API.
options:
  name:
    description: Credential name
    type: str
    required: true
  provider:
    description: Cloud provider (S3, B2, AZURE_BLOB, GOOGLE_CLOUD, etc.)
    type: str
    required: true
  attributes:
    description: Provider-specific credentials
    type: dict
    required: true
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
- name: Manage manage cloud storage credentials
  truenas.storage.cloud_credential:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: example_value
    provider: example_value
    attributes: {}
"""

RETURN = r"""
cloud_credential:
  description: The manage cloud storage credentials details.
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
        provider=dict(type="str", required=True),
        attributes=dict(type="dict", required=True),
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
        items = client.get("cloudsync/credentials")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("cloudsync/credentials/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['name', 'provider', 'attributes']:
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
                            "cloudsync/credentials/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["cloud_credential"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("cloudsync/credentials", payload)
                result["changed"] = True
                result["cloud_credential"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
