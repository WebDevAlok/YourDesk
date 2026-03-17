from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import uvicorn

from yourdesk.broker import create_app
from yourdesk.config import BrokerConfig


def _ensure_binary(name: str) -> None:
    if not shutil.which(name):
        raise SystemExit(f"missing dependency: '{name}' not found in PATH")


def _json_request(url: str, method: str = "GET", body: dict | None = None) -> dict:
    payload = None
    headers = {"accept": "application/json"}
    if body is not None:
        payload = json.dumps(body).encode()
        headers["content-type"] = "application/json"
    req = Request(url, method=method, data=payload, headers=headers)
    with urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def run_broker(args: argparse.Namespace) -> None:
    config = BrokerConfig(host=args.host, port=args.port, token_ttl_seconds=args.ttl, trusted_origin="*")
    app = create_app(config)
    uvicorn.run(app, host=config.host, port=config.port)


def run_host(args: argparse.Namespace) -> None:
    _ensure_binary("x11vnc")
    _ensure_binary("websockify")

    password_file = Path(args.password_file)
    password_file.parent.mkdir(parents=True, exist_ok=True)
    if not password_file.exists():
        _ensure_binary("x11vnc")
        subprocess.run(["x11vnc", "-storepasswd", args.password, str(password_file)], check=True)

    display = args.display
    vnc_port = args.vnc_port
    novnc_port = args.novnc_port

    x11vnc_cmd = [
        "x11vnc",
        "-display",
        display,
        "-rfbauth",
        str(password_file),
        "-forever",
        "-shared",
        "-localhost",
        "-rfbport",
        str(vnc_port),
    ]
    websockify_cmd = ["websockify", str(novnc_port), f"127.0.0.1:{vnc_port}"]

    x11vnc_proc = subprocess.Popen(x11vnc_cmd)
    websockify_proc = subprocess.Popen(websockify_cmd)

    viewer_url = f"http://{args.public_host}:{novnc_port}/vnc.html?host={args.public_host}&port={novnc_port}&password={args.password}"

    register_url = urljoin(args.broker.rstrip("/") + "/", "api/v1/sessions")
    payload = {"alias": args.alias, "viewer_url": viewer_url}
    session = _json_request(register_url, method="POST", body=payload)

    print("YourDesk host session is ready")
    print(f"Support code : {session['code']}")
    print(f"Expires at   : {session['expires_at']}")

    revoke_url = urljoin(args.broker.rstrip("/") + "/", f"api/v1/sessions/{session['code']}")

    def _shutdown(*_: object) -> None:
        try:
            _json_request(revoke_url + f"?secret={session['secret']}", method="DELETE")
        except Exception:
            pass
        for proc in (websockify_proc, x11vnc_proc):
            if proc.poll() is None:
                proc.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    while True:
        time.sleep(1)
        if x11vnc_proc.poll() is not None or websockify_proc.poll() is not None:
            _shutdown()


def run_join(args: argparse.Namespace) -> None:
    lookup_url = urljoin(args.broker.rstrip("/") + "/", f"api/v1/sessions/{args.code}")
    session = _json_request(lookup_url)
    print(f"Connecting to host '{session['alias']}'")
    print(session["viewer_url"])



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="yourdesk")
    sub = parser.add_subparsers(dest="command", required=True)

    broker = sub.add_parser("broker", help="Run broker service")
    broker.add_argument("--host", default="0.0.0.0")
    broker.add_argument("--port", type=int, default=8080)
    broker.add_argument("--ttl", type=int, default=900)
    broker.set_defaults(func=run_broker)

    host = sub.add_parser("host", help="Start local host session")
    host.add_argument("--broker", required=True)
    host.add_argument("--alias", default=os.uname().nodename)
    host.add_argument("--display", default=":0")
    host.add_argument("--vnc-port", type=int, default=5901)
    host.add_argument("--novnc-port", type=int, default=6090)
    host.add_argument("--public-host", required=True)
    host.add_argument("--password", default="changeme")
    host.add_argument("--password-file", default=os.path.expanduser("~/.yourdesk/vnc.pass"))
    host.set_defaults(func=run_host)

    join = sub.add_parser("join", help="Resolve a support code")
    join.add_argument("--broker", required=True)
    join.add_argument("code")
    join.set_defaults(func=run_join)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
