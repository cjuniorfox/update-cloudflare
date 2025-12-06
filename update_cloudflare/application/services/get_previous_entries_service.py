import logging
from update_cloudflare.adaper.repository.dns_entries_repository import DNSRecordsRepository
from update_cloudflare.domain.dns_record import DNSRecord

class GetPreviousEntriesService:
    def __init__(self, dnsrecords_repository: DNSRecordsRepository):
        self.dnsrecords_repository = dnsrecords_repository
        self.logger = logging.getLogger(__name__)

    def execute(self, zone_id: str, dns_record_id: str, record_name: str) -> list[DNSRecord] | None:
        
        self.logger.debug(f"Retrieving last register entry for zone_id: {zone_id}, dns_record_id: {dns_record_id}, record_name: {record_name}")
        records = self.dnsrecords_repository.list_by(zone_id, dns_record_id, record_name)
        self.logger.debug(f"Last register entry retrieved: {records}")
        
        if records is None:
            return None
        return [DNSRecord.from_dict(record) for record in records]