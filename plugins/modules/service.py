#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: service
short_description: Manage TrueNAS services
version_added: "1.0.0"
description:
  - Manage TrueNAS services on a TrueNAS system via the middleware API.
options:
  service:
    description: Service name (smb, nfs, iscsitarget, ssh, snmp, etc.)
    type: str
    required: true
  enabled:
    description: Enable on boot
    type: bool
  started:
    description: Service should be running
    type: bool
extends_documentation_fragment:
  - truenas.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage manage truenas services
  truenas.storage.service:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    service: example_value
"""

RETURN = r"""
result:
  description: Action result.
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
        service=dict(type="str", required=True),
        enabled=dict(type="bool"),
        started=dict(type="bool"),
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
            response = client.post("service", {"service": module.params["service"], "enabled": module.params["enabled"], "started": module.params["started"]})
            result["result"] = response
        result["changed"] = True
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
