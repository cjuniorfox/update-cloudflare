"""Update Cloudflare DNS records with the current IP address."""
from update_cloudflare.main import main
from update_cloudflare.cli import cli

__all__ = ["main", "cli"]
__version__ = "0.1.0"

def get_version():
    return __version__