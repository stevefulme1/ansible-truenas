#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ca
short_description: Manage Certificate Authorities
version_added: "1.0.0"
description:
  - Manage Certificate Authorities on a TrueNAS system via the middleware API.
  - Supports both legacy and TrueNAS SCALE 25.10+ API formats.
options:
  name:
    description: CA name
    type: str
    required: true
  create_type:
    description: Creation method
    type: str
    choices:
      - CA_CREATE_INTERNAL
      - CA_CREATE_IMPORTED
      - CA_CREATE_INTERMEDIATE
      - INTERNAL
      - IMPORTED
      - INTERMEDIATE
  certificate:
    description: PEM-encoded CA certificate
    type: str
  privatekey:
    description: PEM-encoded private key
    type: str
  key_length:
    description: Key length
    type: int
    default: 2048
  digest_algorithm:
    description: Digest algorithm
    type: str
    default: SHA256
  lifetime:
    description: CA lifetime in days
    type: int
    default: 3650
  country:
    description: Country code
    type: str
  state_value:
    description: State/province
    type: str
  city:
    description: City
    type: str
  organization:
    description: Organization
    type: str
  add_to_trusted_store:
    description: Add the CA to the system trusted certificate store
    type: bool
    default: false
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
- name: Manage manage certificate authorities
  truenas.storage.ca:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: example_value
"""

RETURN = r"""
ca:
  description: The manage certificate authorities details.
  returned: success
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.truenas.storage.plugins.module_utils.truenas_api import (
    TrueNASClient,
    TrueNASError,
    truenas_argument_spec,
)

# Map module params to API field names
_field_map = {
    'state_value': 'state',
}


def main():
    argument_spec = truenas_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=True),
        create_type=dict(
            type="str",
            choices=[
                'CA_CREATE_INTERNAL', 'CA_CREATE_IMPORTED', 'CA_CREATE_INTERMEDIATE',
                'INTERNAL', 'IMPORTED', 'INTERMEDIATE',
            ],
        ),
        certificate=dict(type="str"),
        privatekey=dict(type="str", no_log=True),
        key_length=dict(type="int", default=2048, no_log=False),
        digest_algorithm=dict(type="str", default="SHA256"),
        lifetime=dict(type="int", default=3650),
        country=dict(type="str"),
        state_value=dict(type="str"),
        city=dict(type="str"),
        organization=dict(type="str"),
        add_to_trusted_store=dict(type="bool", default=False),
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
        items = client.get("certificateauthority")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("certificateauthority/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            _fields = [
                'name', 'create_type', 'certificate', 'privatekey',
                'key_length', 'digest_algorithm', 'lifetime', 'country',
                'state_value', 'city', 'organization', 'add_to_trusted_store',
            ]
            for key in _fields:
                if module.params.get(key) is not None:
                    api_key = _field_map.get(key, key)
                    payload[api_key] = module.params[key]

            if existing:
                changes = {}
                for key, value in payload.items():
                    if existing.get(key) != value:
                        changes[key] = value
                if changes:
                    if not module.check_mode:
                        existing = client.put(
                            "certificateauthority/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["ca"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("certificateauthority", payload)
                result["changed"] = True
                _sensitive_keys = {'privatekey'}
                safe_payload = {k: v for k, v in payload.items() if k not in _sensitive_keys}
                result["ca"] = existing or safe_payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
