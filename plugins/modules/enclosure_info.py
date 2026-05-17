DOCUMENTATION = r"""
---
module: enclosure_info
short_description: Get enclosure and disk shelf information
version_added: "1.3.0"
description:
  - Retrieve enclosure and disk shelf information from a TrueNAS system
    via the middleware API.
  - Returns a list of enclosures with model, controller, status, and
    element details (disks, PSUs, fans).
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