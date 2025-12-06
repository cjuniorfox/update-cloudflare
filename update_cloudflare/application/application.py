import logging
from update_cloudflare.application.services.get_ipv6_by_ifname_service import GetIPv6ByIfnameService
from update_cloudflare.application.services.filter_public_stable_ipv6_addresses_service import FilterPublicStableIPv6AddressesService
from update_cloudflare.adaper.repository.dns_entries_repository import DNSRecordsRepository
from update_cloudflare.application.services.get_previous_entries_service import GetPreviousEntriesService
from update_cloudflare.application.use_cases.update_ipv6_dns_uc import UpdateIPv6DNSUC
from update_cloudflare.domain.params import Params

class Application:
    def __init__(self, params: Params):
        self.params = params
        self.logger = logging.getLogger(__name__)
        self._beans()

    def run(self):
        # Core logic to update Cloudflare DNS records
        self.logger.debug("Executing Application run method.")
        self.update_ipv6_dns_uc.execute(self.params)

    def _beans(self):
        self.dnsrecords_repository = DNSRecordsRepository(self.params.db_path)
        self.get_ipv6_by_ifname_service = GetIPv6ByIfnameService()
        self.filter_stable_ipv6_addresses_service = FilterPublicStableIPv6AddressesService()
        self.get_previous_entries_service = GetPreviousEntriesService(self.dnsrecords_repository)
        self.update_ipv6_dns_uc = UpdateIPv6DNSUC(
            get_ipv6_by_ifname_service=self.get_ipv6_by_ifname_service,
            filter_public_stable_ipv6_addresses_service=self.filter_stable_ipv6_addresses_service,
            get_previous_entries_service=self.get_previous_entries_service
        )
        self.logger.debug("Beans initialized successfully.")