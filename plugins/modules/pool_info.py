DOCUMENTATION = r"""
---
module: pool_info
short_description: Gather ZFS pool information
version_added: "1.1.0"
description:
  - Retrieve ZFS pool information from a TrueNAS system via the middleware API.
options:
  name:
    description: Pool name to filter results.
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