#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: iscsi_portal
short_description: Manage iSCSI portals
version_added: "1.0.0"
description:
  - Manage iSCSI portals on a TrueNAS system via the middleware API.
options:
  comment:
    description: Portal description
    type: str
  listen:
    description: List of IP:port pairs to listen on
    type: list
    elements: str
    required: true
  discovery_authmethod:
    description: Discovery auth method
    type: str
    default: NONE
    choices: ['NONE', 'CHAP', 'CHAP_MUTUAL']
  discovery_authgroup:
    description: Discovery auth group ID
    type: int
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
- name: Manage manage iscsi portals
  stevefulme1.truenas.iscsi_portal:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    listen:
      - item1
"""

RETURN = r"""
iscsi_portal:
  description: The manage iscsi portals details.
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
        comment=dict(type="str"),
        listen=dict(type="list", elements="str", required=True),
        discovery_authmethod=dict(type="str", default="NONE", choices=['NONE', 'CHAP', 'CHAP_MUTUAL']),
        discovery_authgroup=dict(type="int"),
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
        items = client.get("iscsi/portal")
        if isinstance(items, list):
            for item in items:
                if item.get("comment") == module.params.get("comment"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("iscsi/portal/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['comment', 'listen', 'discovery_authmethod', 'discovery_authgroup']:
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
                            "iscsi/portal/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["iscsi_portal"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("iscsi/portal", payload)
                result["changed"] = True
                result["iscsi_portal"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
