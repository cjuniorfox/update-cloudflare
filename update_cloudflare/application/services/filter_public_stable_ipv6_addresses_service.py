import logging
from update_cloudflare.domain.ipv6_entry import IPv6Entry

class FilterPublicStableIPv6AddressesService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def execute(self, ipv6_addresses: list[IPv6Entry]) -> list[IPv6Entry]:
        self.logger.debug("Filtering for public stable IPv6 addresses.")
        stable_ips = []
        
        stable_ips = [
            ipv6 for ipv6 in ipv6_addresses 
                if 'temporary' not in ipv6.metadata and 'deprecated' not in ipv6.metadata and ipv6.ip.is_global
        ]
        
        if stable_ips:
            self.logger.debug("Found {} stable IPv6 addresses: {}".format(len(stable_ips), [str(ipv6.ip) for ipv6 in stable_ips]))
            return stable_ips
        else:
            self.logger.warning("No public stable IPv6 addresses found.")
        
        """Fallback to any public IPv6 addresses if no stable ones are found."""
        unstable_ips = [ipv6 for ipv6 in ipv6_addresses if ipv6.ip.is_global]
        
        if unstable_ips:
            self.logger.debug(f"Available public IPv6 addresses (not stable): {[str(ipv6.ip) for ipv6 in unstable_ips]}")
            return unstable_ips
        else:
            self.logger.debug("No public IPv6 addresses available.")
            raise RuntimeError("No public IPv6 addresses found.")
        