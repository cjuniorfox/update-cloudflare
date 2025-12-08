from update_cloudflare import main
import update_cloudflare
import argparse

def cli():
    parser = argparse.ArgumentParser(description="Update Cloudflare DNS with current IP.")
    parser.add_argument("record_name", type=str, default="example.com", help="DNS record name to update (default: example.com)")
    parser.add_argument("--ifname", "-i", type=str, default="eth0", help="Network interface name to get the IP from (default: eth0)")
    parser.add_argument("--zone_id", "-z", type=str, default="", help="Cloudflare zone ID (default: empty)")
    parser.add_argument("--dns_record_id", "-d", type=str, default="", help="DNS record ID to update (default: empty)")
    parser.add_argument("--bearer_token", "-t", type=str, default="", help="Cloudflare API bearer token (default: empty)")
    parser.add_argument("--comment", "-c", type=str, default="", help="Add a comment to the DNS record update (default: empty)")
    parser.add_argument("--db-path", "-D", type=str, default=None, required=False, help="Path to the database file (default: empty)")
    parser.add_argument("--log-level", "-l", type=str, default="INFO", help="Set the logging level (default: INFO)")
    parser.add_argument("--version", "-v", action="version", version=f"update-cloudflare {update_cloudflare.get_version()}", help="Show the version and exit")
    args = parser.parse_args()
    
    print(f"Using interface: {args.ifname}")
    main(
        log_level=args.log_level,
        ifname=args.ifname,
        record_name=args.record_name,
        zone_id=args.zone_id,
        dns_record_id=args.dns_record_id,
        bearer_token=args.bearer_token,
        comment=args.comment,
        db_path=args.db_path
    )