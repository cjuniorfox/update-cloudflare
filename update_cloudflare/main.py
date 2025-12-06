from update_cloudflare.domain.params import Params
from update_cloudflare.application.application import Application
import logging

def main(
        log_level: str = "INFO", 
        ifname: str = "eth0", 
        record_name: str = "example.com", 
        zone_id: str = "",
        dns_record_id: str = "",
        bearer_token: str = "",
        comment: str = "",
        db_path: str = None
    ) -> None:
    params = Params(
        log_level=log_level,
        ifname=ifname,
        record_name=record_name,
        zone_id=zone_id,
        dns_record_id=dns_record_id,
        bearer_token=bearer_token,
        comment=comment,
        db_path=db_path
    )
    logging.getLogger().setLevel(params.log_level.upper())
    logging.info(f"Starting update with interface: {params.ifname} for domain record: {params.record_name} with DNS record ID: {params.dns_record_id} and comment: {params.comment}" )
    app = Application(params)
    app.run()