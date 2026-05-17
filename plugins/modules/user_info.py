DOCUMENTATION = r"""
---
module: user_info
short_description: Gather user account information
version_added: "1.1.0"
description:
  - Retrieve user account information from a TrueNAS system via the middleware API.
options:
  username:
    description: Username to filter results.
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