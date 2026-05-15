#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: smart_test
short_description: Run and manage SMART tests
version_added: "1.0.0"
description:
  - Run SMART (Self-Monitoring, Analysis, and Reporting Technology) tests on disks.
  - Query SMART test results for a specific disk.
options:
  disk:
    description: Disk identifier (e.g., sda, sdb)
    type: str
    required: true
  type:
    description: Type of SMART test to run
    type: str
    choices: ['SHORT', 'LONG', 'CONVEYANCE']
    default: SHORT
  state:
    description: Set to present to run a new SMART test.
    type: str
    choices: [present]
    default: present
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Run a short SMART test on sda
  stevefulme1.truenas.smart_test:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    disk: sda
    type: SHORT
    state: present

- name: Run a long SMART test on sdb
  stevefulme1.truenas.smart_test:
    api_url: "https://truenas.example.com"
    api_key: "{{ vault_truenas_api_key }}"
    disk: sdb
    type: LONG
    state: present
"""

RETURN = r"""
job:
  description: The SMART test job details.
  returned: success
  type: dict
results:
  description: Existing SMART test results for the disk.
  returned: success
  type: list
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
        disk=dict(type="str", required=True),
        type=dict(type="str", default="SHORT", choices=["SHORT", "LONG", "CONVEYANCE"]),
        state=dict(type="str", choices=["present"], default="present"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=[["api_key", "username"]],
    )

    client = TrueNASClient(module)
    disk = module.params["disk"]
    test_type = module.params["type"]
    result = dict(changed=False)

    try:
        existing_results = client.get("smart/test/results")
        disk_results = []
        if isinstance(existing_results, list):
            for r in existing_results:
                if r.get("disk") == disk:
                    disk_results.append(r)
        result["results"] = disk_results

        if not module.check_mode:
            payload = {"disks": [disk], "type": test_type}
            job_id = client.post("smart/test", payload)
            if job_id:
                job = client.job_wait(job_id)
                result["job"] = job
        result["changed"] = True

    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
