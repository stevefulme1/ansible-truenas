#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: update_info
short_description: Get available system updates
version_added: "1.3.0"
description:
  - Check for available system updates on a TrueNAS system via the
    middleware API.
  - Returns whether updates are available, the target version,
    changelog, and a list of individual changes.
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
EXAMPLES = r"""
- name: Get update information
  stevefulme1.truenas.update_info:
    host: "{{ truenas_host }}"
  register: result
"""
