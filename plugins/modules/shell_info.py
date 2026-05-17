DOCUMENTATION = r"""
---
module: shell_info
short_description: Gather available user shells
version_added: "1.0.0"
description:
  - Gather available user shells from a TrueNAS system via the middleware API.
options:

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