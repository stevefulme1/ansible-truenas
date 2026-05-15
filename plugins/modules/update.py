#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: update
short_description: Apply system updates
version_added: "1.3.0"
description:
  - Apply pending system updates on a TrueNAS system via the middleware
    API.
  - Checks whether updates are available before attempting to apply.
  - The update operation runs as an async job; the module waits for
    completion.
options:
  reboot:
    description:
      - Whether to reboot the system after applying updates.
    type: bool
    default: false
  train:
    description:
      - Update train to switch to before applying updates.
      - When omitted the current train is used.
    type: str
    required: false
  job_timeout:
    description:
      - Maximum seconds to wait for the update job to finish.
    type: int
    default: 600
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Apply updates without reboot
  stevefulme1.truenas.update:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"

- name: Apply updates and reboot
  stevefulme1.truenas.update:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    reboot: true

- name: Switch train and apply updates
  stevefulme1.truenas.update:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    train: TrueNAS-SCALE-24.10-MASTER
    reboot: true
"""

RETURN = r"""
available:
  description: Whether updates were available.
  returned: always
  type: bool
job:
  description: Job result returned by the update operation.
  returned: when updates were applied
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
        reboot=dict(type="bool", default=False),
        train=dict(type="str", required=False),
        job_timeout=dict(type="int", default=600),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    reboot = module.params["reboot"]
    train = module.params.get("train")
    job_timeout = module.params["job_timeout"]
    result = dict(changed=False)

    try:
        # Switch update train if requested
        if train:
            current = client.get("update/get_trains")
            current_train = current.get("selected")
            if current_train != train:
                if not module.check_mode:
                    client.post(
                        "update/set_train", train
                    )

        # Check whether updates are available
        check = client.post("update/check_available")
        available = bool(
            check.get("status") == "AVAILABLE"
        )
        result["available"] = available

        if not available:
            module.exit_json(**result)

        # In check mode just report that updates would be applied
        if module.check_mode:
            result["changed"] = True
            module.exit_json(**result)

        # Apply updates
        payload = {"reboot": reboot}
        job_id = client.post("update/update", payload)
        job_result = client.job_wait(job_id, timeout=job_timeout)
        result["changed"] = True
        result["job"] = job_result

    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
