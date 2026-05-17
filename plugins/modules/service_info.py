#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: service_info
short_description: Gather service information
version_added: "1.1.0"
description:
  - Retrieve service status and configuration from a TrueNAS system via the middleware API.
options:
  service:
    description: Service name to filter results.
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
EXAMPLES = r"""
- name: Get service information
  stevefulme1.truenas.service_info:
    host: "{{ truenas_host }}"
  register: result
"""
