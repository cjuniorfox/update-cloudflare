import logging
from update_cloudflare.adaper.repository.dns_entries_repository import DNSRecordsRepository
from update_cloudflare.domain.dns_record import DNSRecord

class SaveRegisteredDNSRecordService:
    def __init__(self, dnsrecords_repository: DNSRecordsRepository):
        self.logger = logging.getLogger(__name__)
        self.dnsrecords_repository = dnsrecords_repository

    def execute(self, dns_record: DNSRecord) -> None:
        self.logger.debug(f"Saving registered DNS record: {dns_record}")
        
        self.dnsrecords_repository.save(zone_id=dns_record.zone_id,
                                        dns_record_id=dns_record.dns_record_id,
                                        record_name=dns_record.record_name,
                                        last_ip=str(dns_record.ip))
        
        self.logger.debug("Registered DNS record saved successfully.")