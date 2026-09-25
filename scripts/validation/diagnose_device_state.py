#!/usr/bin/env python3
"""
Cisco Catalyst Center - Fabric Device State Diagnostic

Read-only diagnostic utility for correlating a device's state across:
- Inventory / site assignment
- SDA Fabric Devices
- SDA role-by-management-IP
- Wired-device provisioning

The tool queries Catalyst Center directly for available fabric sites and
allows the operator to select a site and device interactively.

No POST, PUT, PATCH, or DELETE operations are performed.
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from getpass import getpass
from typing import Any
from urllib.parse import urlparse

import requests
from requests import Response, Session
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
import urllib3


DEFAULT_TIMEOUT = 30


@dataclass
class CatalystCenterClient:
    """Small read-only client for the Catalyst Center APIs used by this tool."""

    base_url: str
    username: str
    password: str
    verify: bool | str = True
    timeout: int = DEFAULT_TIMEOUT

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
        self.session = Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def authenticate(self) -> None:
        """Authenticate and add the Catalyst Center token to the session."""
        url = f"{self.base_url}/dna/system/api/v1/auth/token"
        response = self.session.post(
            url,
            auth=HTTPBasicAuth(self.username, self.password),
            verify=self.verify,
            timeout=self.timeout,
        )
        response.raise_for_status()

        token = response.json().get("Token")
        if not token:
            raise RuntimeError("Authentication succeeded but no Token was returned.")

        self.session.headers.update({"X-Auth-Token": token})

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        raise_for_status: bool = True,
    ) -> Response:
        """Perform a GET request against Catalyst Center."""
        response = self.session.get(
            f"{self.base_url}{path}",
            params=params,
            verify=self.verify,
            timeout=self.timeout,
        )
        if raise_for_status:
            response.raise_for_status()
        return response


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only Catalyst Center SDA fabric-device state diagnostic."
    )
