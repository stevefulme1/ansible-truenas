# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module_utils: truenas_api
short_description: TrueNAS REST API client and common argument spec
description:
  - Provides the TrueNASClient class for communicating with the TrueNAS middleware
    REST API v2.0, supporting both API key and username/password authentication.
  - Includes convenience methods for GET, POST, PUT, and DELETE requests, as well
    as async job polling via job_wait. Also exports truenas_argument_spec for
    shared module parameters.
author:
  - Steve Fulmer (@stevefulme1)
"""

import json

from ansible.module_utils.six.moves.urllib.error import HTTPError, URLError
from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible.module_utils.urls import open_url


class TrueNASError(Exception):
    """Exception for TrueNAS API errors."""

    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class TrueNASClient:
    """Client for the TrueNAS middleware REST/WebSocket API."""

    def __init__(self, module):
        self.module = module
        self.baseurl = module.params["api_url"].rstrip("/")
        self.api_key = module.params.get("api_key")
        self.username = module.params.get("username")
        self.password = module.params.get("password")
        self.validate_certs = module.params.get("validate_certs", True)
        self.timeout = module.params.get("api_timeout", 60)

        if not self.api_key and not (self.username and self.password):
            module.fail_json(msg="Either api_key or username/password must be provided.")

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = "Bearer {0}".format(self.api_key)
        return headers

    def _auth(self):
        if self.api_key:
            return None
        return (self.username, self.password)

    def request(self, method, endpoint, data=None):
        url = "{0}/api/v2.0/{1}".format(self.baseurl, endpoint.lstrip("/"))
        headers = self._headers()
        body = json.dumps(data) if data is not None else None

        try:
            response = open_url(
                url,
                method=method,
                headers=headers,
                data=body,
                validate_certs=self.validate_certs,
                timeout=self.timeout,
                url_username=self.username,
                url_password=self.password,
                force_basic_auth=bool(self.username),
            )
            content = response.read()
            if content:
                return json.loads(content)
            return None
        except HTTPError as e:
            raw = e.read()
            try:
                error_body = json.loads(raw)
                error_msg = error_body.get("message", str(error_body))
            except Exception:
                error_msg = raw.decode("utf-8", errors="replace")[:500] if raw else str(e)
            raise TrueNASError(
                "API request failed: {0} {1} - {2}".format(method, url, error_msg),
                status_code=e.code,
            )
        except URLError as e:
            raise TrueNASError(
                "API connection failed: {0} {1} - {2}".format(method, url, e.reason)
            )

    def get(self, endpoint, params=None):
        if params:
            query = urlencode({k: v for k, v in params.items() if v is not None})
            endpoint = "{0}?{1}".format(endpoint, query)
        return self.request("GET", endpoint)

    def post(self, endpoint, data=None):
        return self.request("POST", endpoint, data)

    def put(self, endpoint, data=None):
        return self.request("PUT", endpoint, data)

    def delete(self, endpoint, data=None):
        return self.request("DELETE", endpoint, data)

    def job_wait(self, job_id, timeout=300):
        """Wait for an async job to complete."""
        import time

        elapsed = 0
        interval = 2
        while elapsed < timeout:
            job = self.get("core/get_jobs", params={"id": job_id})
            if job is None or (isinstance(job, list) and not job):
                raise TrueNASError("Job {0} not found".format(job_id))
            if isinstance(job, list) and job:
                job = job[0]
            if job and job.get("state") in ("SUCCESS", "FAILED", "ABORTED"):
                if job["state"] != "SUCCESS":
                    raise TrueNASError(
                        "Job {0} {1}: {2}".format(
                            job_id, job["state"], job.get("error", "Unknown error")
                        )
                    )
                return job.get("result")
            time.sleep(interval)
            elapsed += interval
        raise TrueNASError("Job {0} timed out after {1}s".format(job_id, timeout))


def truenas_argument_spec():
    """Return the common argument spec for TrueNAS modules."""
    return dict(
        api_url=dict(type="str", required=True),
        api_key=dict(type="str", required=False, no_log=True),
        username=dict(type="str", required=False),
        password=dict(type="str", required=False, no_log=True),
        validate_certs=dict(type="bool", default=True),
        api_timeout=dict(type="int", default=60),
    )
