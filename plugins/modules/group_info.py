DOCUMENTATION = r"""
---
module: group_info
short_description: Gather group information
version_added: "1.1.0"
description:
  - Retrieve group information from a TrueNAS system via the middleware API.
options:
  group_name:
    description: Group name to filter results. Uses C(group_name) to avoid collision with Ansible's C(group) keyword.
    type: str

  limit:
    description:
      - Maximum number of results to return.
    type: int
    default: 100
  offset:
    description:
      - Number of results to skip for pagination.
    type: int
    default: 0
extends_documentation_fragment:
  - stevefulme1.truenas.truenas
author:
  - Steve Fulmer (@sfulmer)
"""