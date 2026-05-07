#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: certificate
short_description: Manage TLS certificates
version_added: "1.0.0"
description:
  - Manage TLS certificates on a TrueNAS system via the middleware API.
options:
  name:
    description: Certificate name
    type: str
    required: true
  create_type:
    description: Creation method
    type: str
    choices: ['CERTIFICATE_CREATE_INTERNAL', 'CERTIFICATE_CREATE_IMPORTED', 'CERTIFICATE_CREATE_CSR']
  certificate:
    description: PEM-encoded certificate
    type: str
  privatekey:
    description: PEM-encoded private key
    type: str
  country:
    description: Country code
    type: str
  cert_state:
    description: State/province
    type: str
  city:
    description: City
    type: str
  organization:
    description: Organization
    type: str
  san:
    description: Subject Alternative Names
    type: list
    elements: str
  key_length:
    description: Key length
    type: int
    default: 2048
    choices: [1024, 2048, 4096]
  digest_algorithm:
    description: Digest algorithm
    type: str
    default: SHA256
    choices: ['SHA224', 'SHA256', 'SHA384', 'SHA512']
  lifetime:
    description: Certificate lifetime in days
    type: int
    default: 3650
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
- name: Manage manage tls certificates
  truenas.storage.certificate:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: example_value
"""

RETURN = r"""
certificate:
  description: The manage tls certificates details.
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
        create_type=dict(type="str", choices=['CERTIFICATE_CREATE_INTERNAL', 'CERTIFICATE_CREATE_IMPORTED', 'CERTIFICATE_CREATE_CSR']),
        certificate=dict(type="str"),
        privatekey=dict(type="str", no_log=True),
        country=dict(type="str"),
        cert_state=dict(type="str"),
        city=dict(type="str"),
        organization=dict(type="str"),
        san=dict(type="list", elements="str"),
        key_length=dict(type="int", default=2048, choices=[1024, 2048, 4096]),
        digest_algorithm=dict(type="str", default="SHA256", choices=['SHA224', 'SHA256', 'SHA384', 'SHA512']),
        lifetime=dict(type="int", default=3650),
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
        items = client.get("certificate")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("certificate/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            _field_map = {'cert_state': 'state'}
            _fields = [
                'name', 'create_type', 'certificate', 'privatekey', 'country', 'cert_state', 'city', 'organization', 'san', 'key_length',
                'digest_algorithm', 'lifetime',
            ]
            for key in _fields:
                if module.params.get(key) is not None:
                    payload[_field_map.get(key, key)] = module.params[key]

            if existing:
                changes = {}
                for key, value in payload.items():
                    if existing.get(key) != value:
                        changes[key] = value
                if changes:
                    if not module.check_mode:
                        existing = client.put(
                            "certificate/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["certificate"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("certificate", payload)
                result["changed"] = True
                _sensitive_keys = {'privatekey'}
                safe_payload = {k: v for k, v in payload.items() if k not in _sensitive_keys}
                result["certificate"] = existing or safe_payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
