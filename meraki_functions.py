#!/usr/bin/python3
"""
MerakiSDK
Written by Gustav Larsson
"""

import sys
import requests
from logging_handler import logger

class MerakiSDK:
    """
    Class to handle interactions with Meraki API
    """
    def __init__(self, token, verify=False):
        """ Initial constructor for the class """

        self.base_url = "https://api.meraki.com/api/v1"
        self.headers = { "X-Cisco-Meraki-API-Key": token }
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
                                    data=payload,
                                    headers=self.headers,
                                    verify=self.verify)

        if response.status_code in [400, 401, 403, 404, 429]:

            self._format_logs(40, "Fail", f"Error with request: {response.status_code}")
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

        print(org_id)
        return org_id

    def get_org_networks(self, org_id):
        """ Return available networks in an org """
        response = self._req(f"/organizations/{org_id}/networks")

        return response

    def get_network_devices(self, network_id):
        """ Return devices in a network """
        response = self._req(f"/networks/{network_id}/devices")

        return response

    def create_network(self):
        """ Creates new network in org from given parameters """

        # body = {
        #             "name": "Long Island Office",
        #             "timeZone": "America/Los_Angeles",
        #             "tags": [ "tag1", "tag2" ],
        #             "notes": "Combined network for Long Island Office",
        #             "productTypes": [
        #                 "appliance",
        #                 "switch",
        #                 "camera"
        #             ]
        #         }

if __name__ == "__main__":

    pass
