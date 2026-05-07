#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: config_backup
short_description: Backup or restore system configuration
version_added: "1.0.0"
description:
  - Backup or restore system configuration on a TrueNAS system via the middleware API.
options:
  action:
    description: Action to perform
    type: str
    required: true
    choices: ['backup', 'restore']
  path:
    description: Path for backup file
    type: str
    required: true
  secret:
    description: Encryption passphrase for backup
    type: str
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Backup system configuration
  stevefulme1.truenas.config_backup:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    action: backup
    path: /mnt/tank/backups/truenas-config.tar
    secret: "{{ vault_backup_passphrase }}"

- name: Restore system configuration from backup
  stevefulme1.truenas.config_backup:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    action: restore
    path: /mnt/tank/backups/truenas-config.tar
    secret: "{{ vault_backup_passphrase }}"
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
        action=dict(type="str", required=True, choices=['backup', 'restore']),
        path=dict(type="str", required=True),
        secret=dict(type="str", no_log=True),
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
            response = client.post("system/config", {"action": module.params["action"], "path": module.params["path"], "secret": module.params["secret"]})
            result["result"] = response
        result["changed"] = True
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
