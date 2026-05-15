#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: filesystem_acltemplate
short_description: Manage filesystem ACL templates
version_added: "1.3.0"
description:
  - Create, update, or delete filesystem ACL templates on a TrueNAS
    system via the middleware API.
  - Templates are matched by I(name) for idempotency.
options:
  name:
    description:
      - Name of the ACL template.
    type: str
    required: true
  acl_type:
    description:
      - Type of ACL for this template.
    type: str
    choices:
      - NFS4
      - POSIX1E
  acl:
    description:
      - List of ACL entry dicts defining the template permissions.
      - Each entry should contain the fields expected by the TrueNAS
        ACL template API (e.g. C(tag), C(id), C(perms) or
        C(access)).
    type: list
    elements: dict
  comment:
    description:
      - Optional comment describing the template.
    type: str
  state:
    description:
      - Desired state of the ACL template.
    type: str
    choices:
      - present
      - absent
    default: present
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Create an NFS4 ACL template
  stevefulme1.truenas.filesystem_acltemplate:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: my_nfs4_template
    acl_type: NFS4
    acl:
      - tag: owner@
        type: ALLOW
        perms:
          BASIC: FULL_CONTROL
    comment: Default NFS4 template
    state: present

- name: Delete an ACL template
  stevefulme1.truenas.filesystem_acltemplate:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: my_nfs4_template
    state: absent
"""

RETURN = r"""
acltemplate:
  description: The ACL template object after the operation.
  returned: when state is present
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.stevefulme1.truenas.plugins.module_utils.truenas_api import (
    TrueNASClient,
    TrueNASError,
    truenas_argument_spec,
)


def _build_payload(module):
    """Build API payload from module params."""
    payload = {"name": module.params["name"]}
    if module.params.get("acl_type") is not None:
        payload["acltype"] = module.params["acl_type"]
    if module.params.get("acl") is not None:
        payload["acl"] = module.params["acl"]
    if module.params.get("comment") is not None:
        payload["comment"] = module.params["comment"]
    return payload


def _needs_update(existing, payload):
    """Return True if existing template differs from desired state."""
    for key, value in payload.items():
        if key == "name":
            continue
        if existing.get(key) != value:
            return True
    return False


def main():
    argument_spec = truenas_argument_spec()
    argument_spec.update(
        name=dict(type="str", required=True),
        acl_type=dict(
            type="str", choices=["NFS4", "POSIX1E"]
        ),
        acl=dict(type="list", elements="dict"),
        comment=dict(type="str"),
        state=dict(
            type="str",
            choices=["present", "absent"],
            default="present",
        ),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
        required_if=[
            ["state", "present", ["acl_type", "acl"]],
        ],
    )

    client = TrueNASClient(module)
    name = module.params["name"]
    state = module.params["state"]
    result = dict(changed=False)

    try:
        # Find existing template by name
        existing = None
        templates = client.get("filesystem/acltemplate")
        if isinstance(templates, list):
            for tpl in templates:
                if tpl.get("name") == name:
                    existing = tpl
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete(
                        "filesystem/acltemplate/id/{0}".format(
                            existing["id"]
                        )
                    )
                result["changed"] = True

        else:  # state == present
            payload = _build_payload(module)

            if existing:
                if _needs_update(existing, payload):
                    if not module.check_mode:
                        existing = client.put(
                            "filesystem/acltemplate/id/{0}".format(
                                existing["id"]
                            ),
                            payload,
                        )
                    result["changed"] = True
                result["acltemplate"] = existing
            else:
                if not module.check_mode:
                    created = client.post(
                        "filesystem/acltemplate", payload
                    )
                    result["acltemplate"] = created
                else:
                    result["acltemplate"] = payload
                result["changed"] = True

    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
