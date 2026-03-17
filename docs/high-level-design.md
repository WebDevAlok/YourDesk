# High Level Design (HLD)

## Architecture
YourDesk uses a 3-component architecture:

1. **Broker Service** (FastAPI)
   - Owns session lifecycle.
   - Generates support code + secret.
   - Exposes lookup endpoint for joiners.

2. **Host Agent** (CLI orchestration)
   - Starts `x11vnc` on localhost.
   - Bridges VNC TCP to websocket via `websockify`.
   - Registers viewer URL with Broker.

3. **Join Client** (CLI)
   - Queries broker with support code.
   - Returns noVNC-compatible URL for operator use.

## Design Decisions and Rationale
- **Python + FastAPI**: Rapid delivery, typed API models, easy ops integration.
- **Leverage x11vnc/websockify**: Mature Linux tools reduce protocol implementation risk.
- **Short-lived support codes**: Balances operator usability and attack window.
- **Separate broker and host roles**: Enables centralized control with edge deployment.

## Deployment Topology
- Broker: central VM/container (systemd or Kubernetes).
- Host: end-user Linux endpoint.
- Joiner: support engineer workstation with browser.
