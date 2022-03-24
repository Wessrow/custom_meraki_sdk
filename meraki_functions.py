#!/usr/bin/env python
"""
MerakiSDK
Written by Gustav Larsson
"""

import sys
import json
import requests
from logging_handler import LogHandler

logging = LogHandler("MerakiSDK")
# pylint: disable=line-too-long

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
            logging.format_logs(20, "VerifySSL", "False")
            requests.urllib3.disable_warnings()

    def _req(self, resource, payload=None, method="GET"):
        """ Temp main-function """

        url = f"{self.base_url}{resource}"
        response = requests.request(url=url,
                                    method=method,
                                    data=json.dumps(payload),
                                    headers=self.headers,
                                    verify=self.verify)

        if response.status_code in [401, 403, 429]:

            logging.format_logs(40, "FatalError", f"{response.status_code} - {response.text}")
            sys.exit(1)

        elif response.status_code in [400, 404]:

            logging.format_logs(40, "RequestError", f"{response.status_code} - {response.text}")
            return response

        logging.format_logs(10, "Success", response.status_code)
        return response

    @staticmethod
    def _handle_response(response, log_type, log_message):
        """ Internal function to handle response status_codes and logs """

        if response.status_code in [200,201]:
            logging.format_logs(20, log_type, log_message)

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
            logging.format_logs(40, "Fail", "Orgainzation not found")

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

        self._handle_response(response, "NetworkCreated", f"Network {name} created")
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

        self._handle_response(response, "UserCreated", f"User {name} - {email} created")
        return response

    def add_webhook(self, network_id, name, url, secret):
        """ Adds webhook to network from standard parameters """

        body = {
                    "name": name,
                    "url": url,
                    "sharedSecret": secret
                }

        response = self._req(f"/networks/{network_id}/webhooks/httpServers", body, "POST")

        self._handle_response(response, "WebhookCreated", f"Name {name} - {url} created")
        return response

    def update_alerts(self, network_id, body):
        """ Updates alerts to a network from passed in body """

        response = self._req(f"/networks/{network_id}/alerts/settings", body, "PUT")

        self._handle_response(response, "AlertsCreated", f"Alerts added to {network_id}")
        return response

    def update_s2s_vpn(self, network_id, body):
        """ Updates s2s-vpn for a given network using passed along body """

        response = self._req(f"/networks/{network_id}/appliance/vpn/siteToSiteVpn", body, "PUT")

        self._handle_response(response, "S2sVPNUpdated", f"Site-to-Site VPN for {network_id} updated")
        return response

    def update_firewall_rules(self, network_id, body):
        """ Updates the current appliance l3 firewall settings """

        response = self._req(f"/networks/{network_id}/appliance/firewall/l3FirewallRules", body, "PUT")

        self._handle_response(response, "L3FirewallUpdated", f"L3 Firewall rules for {network_id} updated")
        return response

    def enable_vlans(self, network_id):
        """ Enables VLANs for network """

        body = { "vlansEnabled": True }

        response = self._req(f"/networks/{network_id}/appliance/vlans/settings", body, "PUT")

        self._handle_response(response, "VlansEnabled", f"Vlans enabled on {network_id}")
        return response

    def add_vlan(self, network_id, body):
        """ Adds VLAN """

        response = self._req(f"/networks/{network_id}/appliance/vlans", body, "POST")

        self._handle_response(response, "VlanAdded", f"Vlan id: {body['id']} added to {network_id}")
        return response

    def update_vlan(self, network_id, vlan_id, body):
        """ Update VLAN with new body """

        response = self._req(f"/networks/{network_id}/appliance/vlans/{vlan_id}", body, "PUT")

        self._handle_response(response, "VlanUpdated", f"Vlan id: {body['id']} updated")
        return response

if __name__ == "__main__":

    pass
