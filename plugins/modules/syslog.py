#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: syslog
short_description: Configure remote syslog
version_added: "1.0.0"
description:
  - Configure remote syslog on a TrueNAS system via the middleware API.
options:
  syslogserver:
    description: Remote syslog server
    type: str
  sysloglevel:
    description: Minimum syslog level
    type: str
    choices: ['F_EMERG', 'F_ALERT', 'F_CRIT', 'F_ERR', 'F_WARNING', 'F_NOTICE', 'F_INFO', 'F_DEBUG']
  syslog_transport:
    description: Syslog transport
    type: str
    default: UDP
    choices: ['UDP', 'TCP', 'TLS']
  syslog_certificate:
    description: TLS certificate ID
    type: int
extends_documentation_fragment:
  - truenas.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure remote syslog
  truenas.storage.syslog:
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
from ansible_collections.truenas.storage.plugins.module_utils.truenas_api import (
    TrueNASClient,
    TrueNASError,
    truenas_argument_spec,
)


def main():
    argument_spec = truenas_argument_spec()
    argument_spec.update(
        syslogserver=dict(type="str"),
        sysloglevel=dict(type="str", choices=['F_EMERG', 'F_ALERT', 'F_CRIT', 'F_ERR', 'F_WARNING', 'F_NOTICE', 'F_INFO', 'F_DEBUG']),
        syslog_transport=dict(type="str", default="UDP", choices=['UDP', 'TCP', 'TLS']),
        syslog_certificate=dict(type="int"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        current = client.get("system/advanced")
        payload = {}
        if module.params["syslogserver"] is not None and current.get("syslogserver") != module.params["syslogserver"]:
            payload["syslogserver"] = module.params["syslogserver"]
        if module.params["sysloglevel"] is not None and current.get("sysloglevel") != module.params["sysloglevel"]:
            payload["sysloglevel"] = module.params["sysloglevel"]
        if module.params["syslog_transport"] is not None and current.get("syslog_transport") != module.params["syslog_transport"]:
            payload["syslog_transport"] = module.params["syslog_transport"]
        if module.params["syslog_certificate"] is not None and current.get("syslog_certificate") != module.params["syslog_certificate"]:
            payload["syslog_certificate"] = module.params["syslog_certificate"]
        if payload:
            if not module.check_mode:
                current = client.put("system/advanced", payload)
            result["changed"] = True
        result["config"] = current
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
