#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: service_info
short_description: Gather service information
version_added: "1.1.0"
description:
  - Retrieve service status and configuration from a TrueNAS system via the middleware API.
options:
  service:
    description: Service name to filter results.
    type: str
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: List all services
  stevefulme1.truenas.service_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"

- name: Get a specific service
  stevefulme1.truenas.service_info:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    service: smb
"""

RETURN = r"""
services:
  description: List of services with state and enable status.
  returned: success
  type: list
  elements: dict
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
        service=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    service = module.params.get("service")

    try:
        data = client.get("service")
        services = data if isinstance(data, list) else [data]

        if service:
            services = [s for s in services if s.get("service") == service]

        module.exit_json(changed=False, services=services)
    except TrueNASError as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    main()
