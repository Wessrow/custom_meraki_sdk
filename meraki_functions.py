#!/usr/bin/python3
"""
MerakiSDK
Written by Gustav Larsson
"""

import sys
import json
import requests
from logging_handler import logger

class MerakiSDK:
    """
    Class to handle interactions with Meraki API
    """
    def __init__(self, token, verify=False):
        """ Initial constructor for the class """

        self.base_url = "https://api.meraki.com/api/v1"
        self.headers = {
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "X-Cisco-Meraki-API-Key": token
                    }
        self.verify = verify

        if verify is False:
            self._format_logs(20, "Verify SSL", "False")
            requests.urllib3.disable_warnings()

    @staticmethod
    def _format_logs(level, message_type, message):
        """
        Helper function to format error messages
        """

        info = {"type": message_type,
                    "message": message
        }

        logger.log(level, info)

    def _req(self, resource, payload=None, method="GET"):
        """ Temp main-function """

        url = f"{self.base_url}{resource}"
        response = requests.request(url=url,
                                    method=method,
                                    data=json.dumps(payload),
                                    headers=self.headers,
                                    verify=self.verify)

        if response.status_code in [400, 401, 403, 404, 429]:

            self._format_logs(40, "Fail", f"{response.status_code} - {response.text}")
            sys.exit(1)

        self._format_logs(10, "Success", response.status_code)
        return response

    def get_orgs(self):
        """ Return available orgs """

        response = self._req("/organizations")

        return response

    def get_org_by_name(self, name):
        """ Returns org-id from given org name """

        organizations = self.get_orgs().json()
        org_id = None

        for organization in organizations:
            if organization["name"] == name:
                org_id = organization["id"]

        if org_id is None:
            self._format_logs(40, "Fail", "Orgainzation not found")

        return org_id

    def get_org_networks(self, org_id):
        """ Return available networks in an org """
        response = self._req(f"/organizations/{org_id}/networks")

        return response

    def get_network_devices(self, network_id):
        """ Return devices in a network """
        response = self._req(f"/networks/{network_id}/devices")

        return response

    def create_network(self, org_id, name, tags):
        """ Creates new network in org from given parameters """

        body = {
                    "name": name,
                    "timeZone": "Europe/Stockholm",
                    "tags": tags,
                    "productTypes": [
                        "appliance"
                    ]
                }

        response = self._req(f"/organizations/{org_id}/networks", body, "POST")

        self._format_logs(20, "NetworkCreated", f"Network {name} created")
        return response

    def add_org_admin(self, org_id, email, tags, name=None):
        """ Adds admin to org from given parameters """

        if name is None:
            name = email.split("@")[0]

        body = {
                    "name": name,
                    "email": email,
                    "orgAccess": "none",
                    "tags": tags
                }

        response = self._req(f"/organizations/{org_id}/admins", body, "POST")

        self._format_logs(20, "UserCreated", f"User {name} - {email} created")
        return response

if __name__ == "__main__":

    pass
