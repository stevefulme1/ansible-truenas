#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: smb_status_info
short_description: Gather SMB service status and active sessions
version_added: "1.0.0"
description:
  - Gather SMB service status and active sessions from a TrueNAS system via the middleware API.
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