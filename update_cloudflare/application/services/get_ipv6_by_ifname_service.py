import re
import logging
import ipaddress
from update_cloudflare.domain.ipv6_entry import IPv6Entry

class GetIPv6ByIfnameService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def execute(self, ifname: str) -> list[IPv6Entry]:
        import subprocess

        try:
            self.logger.debug(f"Retrieving IPv6 address for interface: {ifname}")
            result = subprocess.run(
                ['ip', '-6', 'addr', 'show', ifname],
                capture_output=True, text=True, check=True
            )
            # Match full inet6 lines with all metadata
            inet6_lines = re.findall(r'inet6 [0-9a-f:]+/\d+.*', result.stdout)
            if inet6_lines:
                ips = []
                for line in inet6_lines:
                    # Extract IP address
                    ip_match = re.search(r'inet6 ([0-9a-f:]+)/', line)
                    if ip_match:
                        ip_addr = ip_match.group(1)
                        try:
                            ip = ipaddress.IPv6Address(ip_addr)
                            # Extract metadata (everything after the CIDR notation)
                            metadata_match = re.search(r'inet6 [0-9a-f:]+/\d+\s+(.*)', line)
                            metadata = metadata_match.group(1).split() if metadata_match else []
                                
                            ips.append(IPv6Entry(ip, metadata))
                        except ValueError:
                            continue
                
                if ips:
                    self.logger.debug("Found {} IPv6 addresses for interface {}.".format(len(ips), ifname))
                    return ips
                else:
                    raise RuntimeError(
                        f"No IPv6 addresses found for interface {ifname}"
                    )
            else:
                raise RuntimeError(f"No IPv6 address found for interface {ifname}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to retrieve IPv6 address: {e.stderr.strip()}")