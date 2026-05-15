# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
name: stevefulme1.truenas.truenas_inventory
plugin_type: inventory
short_description: Dynamic inventory for TrueNAS VMs
version_added: "1.3.0"
description:
  - Queries the TrueNAS middleware API to build a dynamic inventory of
    virtual machines.
  - VMs are grouped by status (C(running), C(stopped)).
  - Host variables include C(vm_id), C(vcpus), C(memory),
    C(autostart), and C(description).
options:
  api_url:
    description:
      - URL of the TrueNAS API endpoint.
    type: str
    required: true
    env:
      - name: TRUENAS_API_URL
  api_key:
    description:
      - API key for authenticating with TrueNAS.
    type: str
    required: false
    env:
      - name: TRUENAS_API_KEY
  username:
    description:
      - Username for basic authentication.
    type: str
    required: false
    env:
      - name: TRUENAS_USERNAME
  password:
    description:
      - Password for basic authentication.
    type: str
    required: false
    env:
      - name: TRUENAS_PASSWORD
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
author:
  - Steve Fulmer (@sfulmer)
"""

EXAMPLES = r"""
# truenas.yml
plugin: stevefulme1.truenas.truenas_inventory
api_url: https://truenas.example.com
api_key: "{{ lookup('env', 'TRUENAS_API_KEY') }}"

# Usage:
#   ansible-inventory -i truenas.yml --list
"""

import json

from ansible.errors import AnsibleError
from ansible.module_utils.six.moves.urllib.error import (
    HTTPError,
    URLError,
)
from ansible.module_utils.urls import open_url
from ansible.plugins.inventory import BaseInventoryPlugin


class InventoryModule(BaseInventoryPlugin):
    """TrueNAS VM dynamic inventory plugin."""

    NAME = "stevefulme1.truenas.truenas_inventory"

    def verify_file(self, path):
        """Accept files ending in truenas.yml or truenas.yaml."""
        valid = False
        if super().verify_file(path):
            if path.endswith(
                ("truenas.yml", "truenas.yaml")
            ):
                valid = True
        return valid

    def _request(self, method, endpoint):
        """Perform an HTTP request against the TrueNAS API."""
        url = "{0}/api/v2.0/{1}".format(
            self.api_url.rstrip("/"), endpoint.lstrip("/")
        )
        headers = {"Content-Type": "application/json"}

        if self.api_key:
            headers["Authorization"] = "Bearer {0}".format(
                self.api_key
            )

        try:
            response = open_url(
                url,
                method=method,
                headers=headers,
                validate_certs=self.validate_certs,
                timeout=self.api_timeout,
                url_username=self.username,
                url_password=self.password,
                force_basic_auth=bool(self.username),
            )
            return json.loads(response.read())
        except HTTPError as e:
            raise AnsibleError(
                "TrueNAS API error {0}: {1}".format(
                    e.code, e.reason
                )
            )
        except URLError as e:
            raise AnsibleError(
                "Failed to connect to TrueNAS: {0}".format(
                    str(e)
                )
            )

    def parse(self, inventory, loader, path, cache=True):
        """Parse inventory source and populate inventory."""
        super().parse(inventory, loader, path, cache)
        self._read_config_data(path)

        self.api_url = self.get_option("api_url")
        self.api_key = self.get_option("api_key")
        self.username = self.get_option("username")
        self.password = self.get_option("password")
        self.validate_certs = self.get_option(
            "validate_certs"
        )
        self.api_timeout = self.get_option("api_timeout")

        if not self.api_key and not self.username:
            raise AnsibleError(
                "Either api_key or username must be provided."
            )

        vms = self._request("GET", "vm")

        # Create status groups
        self.inventory.add_group("running")
        self.inventory.add_group("stopped")

        for vm in vms:
            name = vm.get("name", "vm-{0}".format(vm["id"]))
            self.inventory.add_host(name)

            # Group by status
            status = vm.get("status", {}).get(
                "state", "UNKNOWN"
            )
            if status == "RUNNING":
                self.inventory.add_child("running", name)
            else:
                self.inventory.add_child("stopped", name)

            # Set host variables
            self.inventory.set_variable(
                name, "vm_id", vm.get("id")
            )
            self.inventory.set_variable(
                name, "vcpus", vm.get("vcpus")
            )
            self.inventory.set_variable(
                name, "memory", vm.get("memory")
            )
            self.inventory.set_variable(
                name, "autostart", vm.get("autostart")
            )
            self.inventory.set_variable(
                name,
                "description",
                vm.get("description", ""),
            )
