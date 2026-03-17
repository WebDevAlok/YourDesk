from dataclasses import dataclass
import os


@dataclass(frozen=True)
class BrokerConfig:
    host: str = os.getenv("YOURDESK_HOST", "0.0.0.0")
    port: int = int(os.getenv("YOURDESK_PORT", "8080"))
    token_ttl_seconds: int = int(os.getenv("YOURDESK_TOKEN_TTL", "900"))
    trusted_origin: str = os.getenv("YOURDESK_TRUSTED_ORIGIN", "*")


@dataclass(frozen=True)
class HostConfig:
    broker_url: str
    display: str = ":0"
    vnc_password_file: str = os.path.expanduser("~/.yourdesk/vnc.pass")
    novnc_port: int = 6090
