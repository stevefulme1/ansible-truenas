#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: nfs_config
short_description: Configure global NFS service settings
version_added: "1.0.0"
description:
  - Configure global NFS service settings on a TrueNAS system via the middleware API.
options:
  servers:
    description: Number of NFS server threads
    type: int
  protocols:
    description: Enabled NFS protocols (NFSv3, NFSv4)
    type: list
    elements: str
  v4_domain:
    description: NFSv4 domain
    type: str
  mountd_port:
    description: mountd bind port
    type: int
  allow_nonroot:
    description: Allow non-root mount requests
    type: bool
  bindip:
    description: IP addresses to bind to
    type: list
    elements: str
extends_documentation_fragment:
  - stevefulme1.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure global nfs service settings
  stevefulme1.storage.nfs_config:
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
        servers=dict(type="int"),
        protocols=dict(type="list", elements="str"),
        v4_domain=dict(type="str"),
        mountd_port=dict(type="int"),
        allow_nonroot=dict(type="bool"),
        bindip=dict(type="list", elements="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        current = client.get("nfs")
        payload = {}
        if module.params["servers"] is not None and current.get("servers") != module.params["servers"]:
            payload["servers"] = module.params["servers"]
        if module.params["protocols"] is not None and current.get("protocols") != module.params["protocols"]:
            payload["protocols"] = module.params["protocols"]
        if module.params["v4_domain"] is not None and current.get("v4_domain") != module.params["v4_domain"]:
            payload["v4_domain"] = module.params["v4_domain"]
        if module.params["mountd_port"] is not None and current.get("mountd_port") != module.params["mountd_port"]:
            payload["mountd_port"] = module.params["mountd_port"]
        if module.params["allow_nonroot"] is not None and current.get("allow_nonroot") != module.params["allow_nonroot"]:
            payload["allow_nonroot"] = module.params["allow_nonroot"]
        if module.params["bindip"] is not None and current.get("bindip") != module.params["bindip"]:
            payload["bindip"] = module.params["bindip"]
        if payload:
            if not module.check_mode:
                current = client.put("nfs", payload)
            result["changed"] = True
        result["config"] = current
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
