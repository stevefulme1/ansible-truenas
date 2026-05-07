#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: reporting
short_description: Configure metrics reporting and export
version_added: "1.0.0"
description:
  - Configure metrics reporting and export on a TrueNAS system via the middleware API.
options:
  graphite_server:
    description: Graphite server hostname
    type: str
  graphite_port:
    description: Graphite port
    type: int
    default: 2003
  graphite_prefix:
    description: Graphite metric prefix
    type: str
  enabled:
    description: Enable reporting
    type: bool
    default: True
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure metrics reporting and export
  stevefulme1.truenas.reporting:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    state: present
"""

RETURN = r"""
config:
  description: Current configuration.
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
        graphite_server=dict(type="str"),
        graphite_port=dict(type="int", default=2003),
        graphite_prefix=dict(type="str"),
        enabled=dict(type="bool", default=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        current = client.get("reporting")
        payload = {}
        if module.params["graphite_server"] is not None and current.get("graphite_server") != module.params["graphite_server"]:
            payload["graphite_server"] = module.params["graphite_server"]
        if module.params["graphite_port"] is not None and current.get("graphite_port") != module.params["graphite_port"]:
            payload["graphite_port"] = module.params["graphite_port"]
        if module.params["graphite_prefix"] is not None and current.get("graphite_prefix") != module.params["graphite_prefix"]:
            payload["graphite_prefix"] = module.params["graphite_prefix"]
        if module.params["enabled"] is not None and current.get("enabled") != module.params["enabled"]:
            payload["enabled"] = module.params["enabled"]
        if payload:
            if not module.check_mode:
                current = client.put("reporting", payload)
            result["changed"] = True
        result["config"] = current
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
