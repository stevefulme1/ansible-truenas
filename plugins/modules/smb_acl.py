#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: smb_acl
short_description: Manage SMB share-level ACLs
version_added: "1.0.0"
description:
  - Manage SMB share-level ACLs on a TrueNAS system via the middleware API.
options:
  share:
    description: Share name
    type: str
    required: true
  acl_entries:
    description: ACL entries (principal, permission, type)
    type: list
    elements: str
    required: true
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage manage smb share-level acls
  stevefulme1.truenas.smb_acl:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    share: example_value
    acl_entries:
      - item1
"""

RETURN = r"""
result:
  description: Action result.
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
        share=dict(type="str", required=True),
        acl_entries=dict(type="list", elements="str", required=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        if not module.check_mode:
            response = client.post("sharing/smb", {"share": module.params["share"], "acl_entries": module.params["acl_entries"]})
            result["result"] = response
        result["changed"] = True
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
