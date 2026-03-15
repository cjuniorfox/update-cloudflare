{
  lib,
  config,
  pkgs,
  ...
}:

with lib;

let
  cfg = config.services.update-cloudflare;

  python3 = pkgs.python3;

  updateCloudflare = python3.pkgs.buildPythonPackage rec {
    pname = "update_cloudflare";
    version = "0.1.0";

    src = pkgs.fetchFromGitHub {
      owner = "cjuniorfox";
      repo = "update-cloudflare";
      rev = "v${version}";
      hash = "sha256-jvvv0uQ8AI9E1L3u6qogDhGQAeXB6hSgVZOnsX1x6Ak=";
    };

    format = "pyproject";

    nativeBuildInputs = with python3.pkgs; [
      setuptools
      wheel
    ];

    propagatedBuildInputs = with python3.pkgs; [
      requests
    ];
    doCheck = false;
  };

  configFile = pkgs.writeText "update-cloudflare/config.ini" ''
    [cloudflare]
    api_token_file = ${cfg.apiTokenFile}
    zone_id = ${cfg.zoneId}
    dns_record_id = ${cfg.dnsRecordId}
    dns_record = ${cfg.dnsRecord}
    interface = ${cfg.interface}
    log_level = ${cfg.logLevel}
    comment = ${cfg.comment or "Updated by NixOS update-cloudflare service"}
  '';

  monitorScript = pkgs.writeShellScript "update-cloudflare-monitor.sh" ''
    #!${pkgs.bash}/bin/bash
    CONFIG_FILE="/etc/update-cloudflare/config.ini"
    PATH="${lib.makeBinPath [ pkgs.gawk pkgs.coreutils-full pkgs.iproute2 ]}:$PATH"

    ini_get() {
      local section=$1 key=$2 file=$3
      awk -F'=' -v s="[$section]" -v k="$key" '
        $0 ~ /^\s*\[/ { found = ($1$2 == s) }
        found && $1 ~ "^\\s*"k"\\s*$" {
          val = $2
          gsub(/^[ \t"]+|[ \t"]+$/,"",val)  # trim spaces/quotes
          print val
          exit
        }
      ' "$file"
    }
  
    DNS_RECORD="$(ini_get cloudflare dns_record "$CONFIG_FILE")"
    INTERFACE="$(ini_get cloudflare interface "$CONFIG_FILE")"
    ZONE_ID="$(ini_get cloudflare zone_id "$CONFIG_FILE")"
    DNS_RECORD_ID="$(ini_get cloudflare dns_record_id "$CONFIG_FILE")"
    LOG_LEVEL="$(ini_get cloudflare log_level "$CONFIG_FILE")"
    COMMENT="$(ini_get cloudflare comment "$CONFIG_FILE")"

    API_TOKEN_FILE="$(ini_get cloudflare api_token_file "$CONFIG_FILE")"
    if [[ -n "$API_TOKEN_FILE" && -f "$API_TOKEN_FILE" ]]; then
      API_TOKEN_RAW="$(< "$API_TOKEN_FILE")"
    else
      echo "Using API token from configuration file."
      API_TOKEN_RAW="$(ini_get cloudflare api_token "$CONFIG_FILE")"
    fi

    API_TOKEN="$( base64 -d <<< "$API_TOKEN_RAW" || echo "$API_TOKEN_RAW" )"

    while true; do
      ${updateCloudflare}/bin/update-cloudflare \
        "$DNS_RECORD" \
        --ifname "$INTERFACE" \
        --zone_id "$ZONE_ID" \
        --dns_record_id "$DNS_RECORD_ID" \
        --bearer_token "$API_TOKEN" \
        --comment "$COMMENT" \
        --log-level "$LOG_LEVEL"
      
      sleep 300  # Wait for 5 minutes before the next update
    done
  '';
in
{
  options.services.update-cloudflare = {
    enable = mkEnableOption "Enable the update-cloudflare service.";
    interface = mkOption {
      type = types.str;
      description = "Network interface to monitor for IPv6 addresses.";
    };
    logLevel = mkOption {
      type = types.enum [
        "DEBUG"
        "INFO"
        "WARNING"
        "ERROR"
        "CRITICAL"
      ];
      default = "INFO";
      description = "Logging level. One of: DEBUG, INFO, WARNING, ERROR, CRITICAL.";
    };
    apiTokenFile = mkOption {
      type = types.path;
      description = "Path to a file containing the Cloudflare API token. The API token can be encoded in base64 or stored as plain text. If not provided.";
      default = null;
    };
    comment = mkOption {
      type = types.str;
      description = "Optional comment to add to the DNS record update.";
      default = null;
    };
    zoneId = mkOption {
      type = types.str;
      description = "Cloudflare Zone ID for the domain.";
    };
    dnsRecordId = mkOption {
      type = types.str;
      description = "Cloudflare DNS Record ID to update.";
    };
    dnsRecord = mkOption {
      type = types.str;
      description = "The DNS record (hostname) to update.";
    };
  };

  config = mkIf cfg.enable {
    environment.etc."update-cloudflare/config.ini".source = configFile;
    systemd.services.update-cloudflare = {
      description = "Update Cloudflare DNS record for ${cfg.dnsRecord}";
      after = [ "network-online.target" ];
      wants = [ "network-online.target" ];
      unitConfig.PartOf = [ "multi-user.target" ];
      serviceConfig = {
        Type = "simple";
        ExecStart = "${monitorScript}";
        Restart = "always";
        RestartSec = 10;
      };
      wantedBy = [ "multi-user.target" ];
    };
  };
}