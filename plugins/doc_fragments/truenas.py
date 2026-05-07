# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment:

    DOCUMENTATION = r"""
options:
  api_url:
    description:
      - URL of the TrueNAS API endpoint.
      - For example, C(https://truenas.example.com).
    type: str
    required: true
  api_key:
    description:
      - API key for authenticating with TrueNAS.
      - Mutually exclusive with I(username) and I(password).
    type: str
    required: false
  username:
    description:
      - Username for basic authentication.
      - Must be used together with I(password).
    type: str
    required: false
  password:
    description:
      - Password for basic authentication.
      - Must be used together with I(username).
    type: str
    required: false
    no_log: true
  validate_certs:
    description:
      - Whether to validate SSL/TLS certificates.
    type: bool
    default: true
  api_timeout:
    description:
      - Timeout in seconds for API requests.
    type: int
    default: 60
"""
