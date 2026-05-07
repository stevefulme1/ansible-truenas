#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ssh
short_description: Configure SSH service
version_added: "1.0.0"
description:
  - Configure SSH service on a TrueNAS system via the middleware API.
options:
  port:
    description: SSH port
    type: int
    default: 22
  rootlogin:
    description: Allow root login
    type: bool
    default: False
  passwordauth:
    description: Allow password authentication
    type: bool
    default: True
  kerberosauth:
    description: Enable Kerberos authentication
    type: bool
    default: False
  tcpfwd:
    description: Allow TCP forwarding
    type: bool
    default: False
  compression:
    description: Enable compression
    type: bool
    default: False
  sftp_log_level:
    description: SFTP log level
    type: str
  sftp_log_facility:
    description: SFTP log facility
    type: str
extends_documentation_fragment:
  - stevefulme1.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage configure ssh service
  stevefulme1.storage.ssh:
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
        port=dict(type="int", default=22),
        rootlogin=dict(type="bool", default=False),
        passwordauth=dict(type="bool", default=True),
        kerberosauth=dict(type="bool", default=False),
        tcpfwd=dict(type="bool", default=False),
        compression=dict(type="bool", default=False),
        sftp_log_level=dict(type="str"),
        sftp_log_facility=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    result = dict(changed=False)

    try:
        current = client.get("ssh")
        payload = {}
        if module.params["port"] is not None and current.get("port") != module.params["port"]:
            payload["port"] = module.params["port"]
        if module.params["rootlogin"] is not None and current.get("rootlogin") != module.params["rootlogin"]:
            payload["rootlogin"] = module.params["rootlogin"]
        if module.params["passwordauth"] is not None and current.get("passwordauth") != module.params["passwordauth"]:
            payload["passwordauth"] = module.params["passwordauth"]
        if module.params["kerberosauth"] is not None and current.get("kerberosauth") != module.params["kerberosauth"]:
            payload["kerberosauth"] = module.params["kerberosauth"]
        if module.params["tcpfwd"] is not None and current.get("tcpfwd") != module.params["tcpfwd"]:
            payload["tcpfwd"] = module.params["tcpfwd"]
        if module.params["compression"] is not None and current.get("compression") != module.params["compression"]:
            payload["compression"] = module.params["compression"]
        if module.params["sftp_log_level"] is not None and current.get("sftp_log_level") != module.params["sftp_log_level"]:
            payload["sftp_log_level"] = module.params["sftp_log_level"]
        if module.params["sftp_log_facility"] is not None and current.get("sftp_log_facility") != module.params["sftp_log_facility"]:
            payload["sftp_log_facility"] = module.params["sftp_log_facility"]
        if payload:
            if not module.check_mode:
                current = client.put("ssh", payload)
            result["changed"] = True
        result["config"] = current
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
