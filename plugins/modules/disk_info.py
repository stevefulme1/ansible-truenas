DOCUMENTATION = r"""
---
module: disk_info
short_description: Gather disk information
version_added: "1.0.0"
description:
  - Gather disk information from a TrueNAS system via the middleware API.
options:
  name:
    description: Specific disk name to query
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