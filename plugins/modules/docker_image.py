#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: docker_image
short_description: Pull or remove Docker images
version_added: "1.0.0"
description:
  - Pull or remove Docker images on a TrueNAS system via the middleware API.
options:
  image:
    description: Image name (e.g., nginx)
    type: str
    required: true
  tag:
    description: Image tag
    type: str
    default: latest
  state:
    description: Desired state of the resource.
    type: str
    choices: [present, absent]
    default: present
extends_documentation_fragment:
  - stevefulme1.storage.truenas
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
- name: Manage pull or remove docker images
  stevefulme1.storage.docker_image:
    api_url: https://truenas.example.com
    api_key: "{{ vault_truenas_api_key }}"
    image: example_value
"""

RETURN = r"""
docker_image:
  description: The pull or remove docker images details.
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
        image=dict(type="str", required=True),
        tag=dict(type="str", default="latest"),
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
        items = client.get("app/image")
        if isinstance(items, list):
            for item in items:
                if item.get("repo_tag") == module.params.get("repo_tag"):
                    existing = item
                    break

        if state == "absent":
            if existing:
                if not module.check_mode:
                    client.delete("app/image/id/{0}".format(existing["id"]))
                result["changed"] = True
        else:
            payload = {}
            for key in ['image', 'tag']:
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
                            "app/image/id/{0}".format(existing["id"]), changes
                        )
                    result["changed"] = True
                result["docker_image"] = existing
            else:
                if not module.check_mode:
                    existing = client.post("app/image", payload)
                result["changed"] = True
                result["docker_image"] = existing or payload
    except TrueNASError as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
