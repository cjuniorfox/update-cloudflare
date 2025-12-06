from ipaddress import IPv6Address
import logging
from update_cloudflare.application.services.get_ipv6_by_ifname_service import GetIPv6ByIfnameService
from update_cloudflare.application.services.filter_public_stable_ipv6_addresses_service import FilterPublicStableIPv6AddressesService
from update_cloudflare.application.services.get_previous_entries_service import GetPreviousEntriesService
from update_cloudflare.domain.dns_record import DNSRecord
from update_cloudflare.domain.ipv6_entry import IPv6Entry
from update_cloudflare.domain.params import Params

class UpdateIPv6DNSUC:
    def __init__(
            self,
            get_ipv6_by_ifname_service : GetIPv6ByIfnameService,
            filter_public_stable_ipv6_addresses_service : FilterPublicStableIPv6AddressesService,
            get_previous_entries_service: GetPreviousEntriesService
        )-> None:
        self.logger = logging.getLogger(__name__)
        self.get_ipv6_by_ifname_service = get_ipv6_by_ifname_service
        self.filter_public_stable_ipv6_addresses_service = filter_public_stable_ipv6_addresses_service
        self.get_previous_entries_service = get_previous_entries_service
    
    def execute(self, params: Params) -> None:
        
        self.logger.debug("Starting UpdateIPv6DNSUC use case execution.")
        
        ips = self.get_ipv6_by_ifname_service.execute(params.ifname)
        stable_public_ips = self.filter_public_stable_ipv6_addresses_service.execute(ips)
        
        previous_entries = self.get_previous_entries_service.execute(params.zone_id, params.dns_record_id, params.record_name)
        
        new_ips = self._new_ips(stable_public_ips, previous_entries)
        
        # Further logic to update Cloudflare DNS with the retrieved IPv6 address
        self.logger.debug(f"Retrieved IPv6 information: {new_ips}")
        
    def _new_ips(self, stable_public_ips : list[IPv6Entry], previous_entries : list[DNSRecord]) -> list[IPv6Address]:
        if previous_entries:
            return [
                ipv6.ip for ipv6 in stable_public_ips 
                    if str(ipv6.ip) not in [str(entry.ip) for entry in previous_entries]
            ]
        else:
            self.logger.debug("No previous DNS entries found. Considering all stable public IPv6 addresses as new.")
            return [ipv6.ip for ipv6 in stable_public_ips]