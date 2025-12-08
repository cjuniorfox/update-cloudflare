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
      sha256 = lib.fakeHash;
    };

    format = "pyproject";

    nativeBuildInputs = with python3.pkgs; [
      setuptools
      wheel
    ];

    propagatedBuildInputs = [ ];
    doCheck = false;
  };

  encodedApiToken = pkgs.runCommand "encoded-api-token" {} ''
    ${pkgs.base64}/bin/base64 -w 0 <<< '${cfg.apiToken}' | ${pkgs.coreutils}/bin/tr -d '\n' > $out
  '';

  configFile = pkgs.writeText "update-cloudflare/config.ini" ''
    [cloudflare]
    api_token = ${builtins.readFile encodedApiToken}
    zone_id = ${cfg.zoneId}
    dns_record_id = ${cfg.dnsRecordId}
    dns_record = ${cfg.dnsRecord}
    interface = ${cfg.interface}
    log_level = ${cfg.logLevel}
  '';

  monitorScript = pkgs.writeShellScript "update-cloudflare-monitor.sh" ''
    #!${pkgs.bash}/bin/bash
    CONFIG_FILE="/etc/update-cloudflare/config.ini"
    PATH="${lib.makeBinPath [ pkgs.gawk pkgs.coreutils-full pkgs.iproute2 ]}:$PATH"

    ini_get() {
      local section=$1 key=$2 file=$3
      awk -F'=' -v s="[$section]" -v k="$key" '
        $0 ~ /^\s*\[/ { in = ($1$2 == s) }                # track section
        in && $1 ~ "^\\s*"k"\\s*$" {
          val = $2
          gsub(/^[ \t"]+|[ \t"]+$/,"",val)               # trim spaces/quotes
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

    API_TOKEN_RAW="$(ini_get cloudflare api_token "$CONFIG_FILE")"
    API_TOKEN="$( base64 -d <<< "$API_TOKEN_RAW" )"

    while true; do
      ${updateCloudflare}/bin/update-cloudflare \
        "$DNS_RECORD" \
        --interface "$INTERFACE" \
        --zone-id "$ZONE_ID" \
        --dns-record-id "$DNS_RECORD_ID" \
        --api-token "$API_TOKEN" \
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
    apiToken = mkOption {
      type = types.str;
      description = "Cloudflare API token with permissions to edit DNS records.";
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