import ipaddress

class IPv6Entry:
    def __init__(self, ip: ipaddress.IPv6Address, metadata: list[str]):
        self._ip = ip
        self._metadata = metadata

    @property
    def ip(self) -> ipaddress.IPv6Address:
        return self._ip
    
    @property
    def metadata(self) -> list[str]:
        return self._metadata
    
    def __str__(self) -> str:
        return "IPv6Address(ip={}, metadata={})".format(self._ip, self._metadata)
    
    def __repr__(self) -> str:
        return self.__str__()