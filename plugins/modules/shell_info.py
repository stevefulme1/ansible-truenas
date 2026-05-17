#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

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
EXAMPLES = r"""
- name: Get shell information
  stevefulme1.truenas.shell_info:
    host: "{{ truenas_host }}"
  register: result
"""
