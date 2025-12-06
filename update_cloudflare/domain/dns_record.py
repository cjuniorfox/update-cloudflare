import ipaddress

class DNSRecord:
    def __init__(
        self,
        zone_id: str,
        dns_record_id: str,
        record_name: str,
        ip: ipaddress.IPv6Address,
    ) -> None:
        self._zone_id = zone_id
        self._dns_record_id = dns_record_id
        self._record_name = record_name
        self._ip = ip
    
    @property
    def zone_id(self) -> str:
        return self._zone_id
    
    @property
    def dns_record_id(self) -> str:
        return self._dns_record_id
    
    @property
    def record_name(self) -> str:
        return self._record_name
    
    @property
    def ip(self) -> ipaddress.IPv6Address:
        return self._ip
    
    def to_dict(self) -> dict:
        return {
            "zone_id": self.zone_id,
            "dns_record_id": self.dns_record_id,
            "record_name": self.record_name,
            "ip": str(self.ip)
        }
        
    @staticmethod
    def from_dict(data: dict) -> 'DNSRecord':
        return DNSRecord(
            zone_id=data["zone_id"],
            dns_record_id=data["dns_record_id"],
            record_name=data["record_name"],
            ip=ipaddress.IPv6Address(data["ip"])
        )
        
    def __str__(self) -> str:
        return f"DNSRegister(zone_id={self.zone_id}, dns_record_id={self.dns_record_id}, record_name={self.record_name}, ip={self.ip})"
    
    def __repr__(self) -> str:
        return self.__str__()