# Update Cloudflare

A utility for updating Cloudflare DNS records with your current IPv6 address automatically.

## Installation

### Via pip

```bash
pip install -e .
```

### Via NixOS Module

You can use the NixOS module to automatically run this as a systemd service.

## Usage

### CLI

Basic usage - update a DNS record with default interface:

```bash
update-cloudflare example.com \
  --ifname eth0 \
  --zone-id your-zone-id \
  --dns-record-id your-record-id \
  --bearer-token your-api-token
```

Or using short options:

```bash
update-cloudflare example.com \
  -i eth0 \
  -z your-zone-id \
  -d your-record-id \
  -t your-api-token
```

#### CLI Options

- `record_name` - DNS record name to update (positional argument)
- `-i, --ifname` - Network interface to get IPv6 from (default: `eth0`)
- `-z, --zone-id` - Cloudflare Zone ID
- `-d, --dns-record-id` - Cloudflare DNS Record ID to update
- `-t, --bearer-token` - Cloudflare API bearer token
- `-c, --comment` - Optional comment to add to the DNS record update
- `-D, --db-path` - Path to database file for tracking previous entries
- `-l, --log-level` - Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: `INFO`)
- `-v, --version` - Show version and exit

#### Example with all options

```bash
update-cloudflare example.com \
  -i eth0 \
  -z abc123 \
  -d def456 \
  -t your-api-token \
  -c "Auto-updated by update-cloudflare" \
  -D /var/lib/update-cloudflare/db.json \
  -l DEBUG
```

### NixOS Service

This repository includes a NixOS module that sets up a systemd service to automatically update your Cloudflare DNS records.

#### What the NixOS Module Does

The module creates a background service that:

- Monitors a specified network interface for IPv6 address changes
- Automatically updates Cloudflare DNS records with your current IPv6 address
- Checks and updates every 5 minutes
- Base64-encodes your API token for security
- Runs continuously with automatic restart on failure

#### How to Use the NixOS Module

**1. Configure the service in your `configuration.nix`:**

```nix

imports = [ 
  (import (builtins.fetchurl {
    url = "https://github.com/cjuniorfox/update-cloudflare/blob/v0.1.0/nixos/update-cloudflare.nix";
    sha256 = "0nzw1f8zbxnjwxprimwyjcf2xycw0pqdr643b6m9gjqa71jln2as";
    }))
];

services.update-cloudflare = {
  enable = true;
  interface = "eth0";                    # Network interface to monitor
  dnsRecord = "example.com";              # Your domain name
  apiToken = "your-cloudflare-api-token";
  zoneId = "your-cloudflare-zone-id";
  dnsRecordId = "your-cloudflare-record-id";
  logLevel = "INFO";                      # DEBUG, INFO, WARNING, ERROR, CRITICAL
};
```

**2. Rebuild and switch:**

```bash
sudo nixos-rebuild switch
```

#### Getting Your Cloudflare Credentials

1. **API Token**: Go to Cloudflare Dashboard → Account → API Tokens → Create Token (with DNS edit permissions)
2. **Zone ID**: Dashboard → Your Domain → Overview (right sidebar)
3. **Record ID**: Dashboard → Your Domain → DNS → Click your record → Copy the ID from the URL or API

#### Configuration Options

- `enable` - Enable/disable the service (default: `false`)
- `interface` - Network interface to monitor for IPv6 changes (required)
- `dnsRecord` - The DNS record hostname to update (required)
- `apiToken` - Cloudflare API token (required)
- `zoneId` - Cloudflare Zone ID (required)
- `dnsRecordId` - Cloudflare DNS Record ID (required)
- `logLevel` - Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: `INFO`)

## Features

- Update DNS records automatically
- Support for IPv6 address monitoring
- Error handling and logging
- Secure API token encoding
- NixOS integration for declarative configuration

## Requirements

- Cloudflare API access
- Python 3.12+ (for pip installation)
- NixOS (for module usage)

## License

MIT
