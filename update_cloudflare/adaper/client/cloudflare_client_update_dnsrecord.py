import ipaddress
import logging
import requests

class CloudflareClientUpdateDNSRecordApi:
    def __init__(self, api_token: str) -> None:
        self.api_token = api_token
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.logger = logging.getLogger(__name__)

    def update_dns_record(self, zone_id: str, dns_record_id: str, record_name: str, ip: ipaddress.IPv6Address) -> dict:
        url = f"{self.base_url}/zones/{zone_id}/dns_records/{dns_record_id}"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        data = {
            "type": "AAAA",
            "name": record_name,
            "content": str(ip),
            "ttl": 1,
            "proxied": False
        }

        self.logger.debug(f"Sending request to update DNS record: {data}")

        response = requests.put(url, json=data, headers=headers)

        if response.status_code == 200:
            self.logger.debug(f"Successfully updated DNS record: {response.json()}")
            return response.json()
        else:
            self.logger.error(f"Failed to update DNS record: {response.status_code} - {response.text}")
            response.raise_for_status()