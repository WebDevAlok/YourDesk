# YourDesk User Manual

## Install

### Ubuntu/Debian
```bash
sudo apt install ./yourdesk_1.0.0_all.deb
```

### RHEL/Fedora
```bash
sudo dnf install ./yourdesk-1.0.0-1.noarch.rpm
```

### Arch Linux
```bash
makepkg -si
```

## Broker Setup
```bash
yourdesk broker --host 0.0.0.0 --port 8080 --ttl 900
```

## Host Session
```bash
yourdesk host \
  --broker http://broker.example.com:8080 \
  --public-host host.example.com \
  --alias "Finance-Laptop" \
  --password "StrongTemporaryPassword"
```

Copy the displayed support code to the support engineer.

## Join Session
```bash
yourdesk join --broker http://broker.example.com:8080 123-456-789
```

Open the returned URL in a browser with noVNC assets available.

## Run as Service (host)
- Install `packaging/systemd/yourdesk-host.service`.
- Override ExecStart with your broker/public host parameters.
- Enable with:
```bash
sudo systemctl enable --now yourdesk-host
```

## Troubleshooting
- Ensure `x11vnc` and `websockify` are installed.
- Verify firewall access to broker (8080) and host noVNC port (default 6090).
- For X11 permission issues, run host under the logged-in desktop user.
