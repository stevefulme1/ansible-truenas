#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

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
EXAMPLES = r"""
- name: Get enclosure information
  stevefulme1.truenas.enclosure_info:
    host: "{{ truenas_host }}"
  register: result
"""
