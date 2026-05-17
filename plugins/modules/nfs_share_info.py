DOCUMENTATION = r"""
---
module: nfs_share_info
short_description: Gather NFS export information
version_added: "1.1.0"
description:
  - Retrieve NFS export configuration from a TrueNAS system via the middleware API.
options:
  id:
    description: NFS export ID to filter results.
    type: int

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