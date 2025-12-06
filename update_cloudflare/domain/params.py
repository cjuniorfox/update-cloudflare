class Params:
    def __init__(
            self, 
            log_level: str = "INFO", 
            ifname: str = "eth0", 
            record_name: str = "example.com",
            zone_id: str = "",
            dns_record_id: str = "",
            bearer_token: str = "",
            comment: str = "",
            db_path: str | None = None
        ) -> None:
        self._log_level = log_level
        self._ifname = ifname
        self._record_name = record_name
        self._zone_id = zone_id
        self._dns_record_id = dns_record_id
        self._bearer_token = bearer_token
        self._comment = comment
        self._db_path = db_path

    @property
    def log_level(self) -> str:
        return self._log_level
    
    @property
    def ifname(self) -> str:
        return self._ifname
    
    @property
    def record_name(self) -> str:
        return self._record_name
    
    @property
    def zone_id(self) -> str:
        return self._zone_id
    
    @property
    def dns_record_id(self) -> str:
        return self._dns_record_id
    
    @property
    def bearer_token(self) -> str:
        return self._bearer_token
    
    @property
    def comment(self) -> str:
        return self._comment
    
    @property
    def db_path(self) -> str | None:
        return self._db_path
    
    def __repr__(self) -> str:
        return (
            f"Params(log_level={self.log_level}, ifname={self.ifname}, "
            f"record_name={self.record_name}, zone_id={self.zone_id}, "
            f"dns_record_id={self.dns_record_id}, bearer_token=****, "
            f"comment={self.comment}, db_path={self.db_path})"
        )