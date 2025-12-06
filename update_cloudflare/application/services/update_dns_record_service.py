import ipaddress
import logging
from update_cloudflare.adaper.client.cloudflare_client_update_dnsrecord import CloudflareClientUpdateDNSRecordApi
from update_cloudflare.domain.dns_record import DNSRecord

class UpdateDNSRecordService:
    def __init__(self, cloudflare_client_update_dnsrecord: CloudflareClientUpdateDNSRecordApi) -> None:
        self.cloudflare_client_update_dnsrecord = cloudflare_client_update_dnsrecord
        self.logger = logging.getLogger(__name__)
    
    def execute(self, zone_id: str, dns_record_id: str, record_name: str, ips: list[ipaddress.IPv6Address]) -> DNSRecord:

        self.logger.debug(f"Updating DNS record {dns_record_id} in zone {zone_id} with name {record_name} to IPs: {ips}")
        
        first_ip : ipaddress.IPv6Address = ips[0] if ips else None
        
        if first_ip is None:
            self.logger.error("No IP addresses provided to update the DNS record.")
            raise ValueError("At least one IP address must be provided to update the DNS record.")
        
        # Call the Cloudflare API to update the DNS record
        self.cloudflare_client_update_dnsrecord.update_dns_record(
            zone_id=zone_id,
            dns_record_id=dns_record_id,
            record_name=record_name,
            ip=first_ip
        )
        
        self.logger.debug(f"DNS record {dns_record_id} in zone {zone_id} updated successfully with IP {first_ip}.")

        return DNSRecord(zone_id=zone_id, dns_record_id=dns_record_id, record_name=record_name, ip=first_ip)