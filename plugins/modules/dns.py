#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dns
short_description: Configure DNS settings
version_added: "1.0.0"
description:
  - Configure DNS settings on a TrueNAS system via the middleware API.
options:
  nameserver1:
    description: Primary DNS server
    type: str
  nameserver2:
    description: Secondary DNS server
    type: str
  nameserver3:
    description: Tertiary DNS server
    type: str
  domain:
    description: Default domain
    type: str
  search_domains:
    description: DNS search domains
    type: list
    elements: str
extends_documentation_fragment:
  - stevefulme1.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure dns settings
  stevefulme1.storage.dns:
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
from ansible_collections.stevefulme1.storage.plugins.module_utils.truenas_api import (
    TrueNASClient,
    TrueNASError,
    truenas_argument_spec,
)


def main():
    argument_spec = truenas_argument_spec()
    argument_spec.update(
        nameserver1=dict(type="str"),
        nameserver2=dict(type="str"),
        nameserver3=dict(type="str"),
        domain=dict(type="str"),
        search_domains=dict(type="list", elements="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        current = client.get("network/configuration")
        payload = {}
        if module.params["nameserver1"] is not None and current.get("nameserver1") != module.params["nameserver1"]:
            payload["nameserver1"] = module.params["nameserver1"]
        if module.params["nameserver2"] is not None and current.get("nameserver2") != module.params["nameserver2"]:
            payload["nameserver2"] = module.params["nameserver2"]
        if module.params["nameserver3"] is not None and current.get("nameserver3") != module.params["nameserver3"]:
            payload["nameserver3"] = module.params["nameserver3"]
        if module.params["domain"] is not None and current.get("domain") != module.params["domain"]:
            payload["domain"] = module.params["domain"]
        if module.params["search_domains"] is not None and current.get("search_domains") != module.params["search_domains"]:
            payload["search_domains"] = module.params["search_domains"]
        if payload:
            if not module.check_mode:
                current = client.put("network/configuration", payload)
            result["changed"] = True
        result["config"] = current
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
