#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: alert_service
short_description: Configure alert notification services
version_added: "1.0.0"
description:
  - Configure alert notification services on a TrueNAS system via the middleware API.
options:
  name:
    description: Alert service name
    type: str
    required: true
  type:
    description: Service type
    type: str
    required: true
    choices: ['Mail', 'Slack', 'PagerDuty', 'SNMPTrap', 'Mattermost', 'OpsGenie', 'VictorOps', 'Telegram']
  attributes:
    description: Service-specific configuration
    type: dict
    required: true
  enabled:
    description: Enable the alert service
    type: bool
    default: True
  level:
    description: Minimum alert level
    type: str
    default: WARNING
    choices: ['INFO', 'NOTICE', 'WARNING', 'ERROR', 'CRITICAL', 'ALERT', 'EMERGENCY']
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
- name: Manage configure alert notification services
  stevefulme1.truenas.alert_service:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    name: example_value
    type: example_value
    attributes: {}
"""

RETURN = r"""
alert_service:
  description: The configure alert notification services details.
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
        name=dict(type="str", required=True),
        type=dict(type="str", required=True, choices=['Mail', 'Slack', 'PagerDuty', 'SNMPTrap', 'Mattermost', 'OpsGenie', 'VictorOps', 'Telegram']),
        attributes=dict(type="dict", required=True),
        enabled=dict(type="bool", default=True),
        level=dict(type="str", default="WARNING", choices=['INFO', 'NOTICE', 'WARNING', 'ERROR', 'CRITICAL', 'ALERT', 'EMERGENCY']),
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
        items = client.get("alertservice")
        if isinstance(items, list):
            for item in items:
                if item.get("name") == module.params.get("name"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("alertservice/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['name', 'type', 'attributes', 'enabled', 'level']:
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
                            "alertservice/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["alert_service"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("alertservice", payload)
                result["changed"] = True
                result["alert_service"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
