# YourDesk Requirements Specification

## 1. Product Vision
Provide Linux-first remote support software with AnyDesk-like workflow:
1. Host starts a support session.
2. A short code is generated.
3. Technician joins using the code and gains remote desktop control.

## 2. Functional Requirements
- FR-1: Broker shall generate unique one-time support codes with TTL.
- FR-2: Host agent shall register and revoke sessions with the broker.
- FR-3: Host agent shall expose desktop stream via VNC and websocket bridge.
- FR-4: Join client shall resolve support code and provide viewer endpoint.
- FR-5: System shall support unattended mode through persistent service startup.
- FR-6: Session metadata shall include alias and expiry for auditability.

## 3. Non-Functional Requirements
- NFR-1: Linux distributions supported: Debian/Ubuntu, RHEL/Fedora, Arch.
- NFR-2: Session setup under 10 seconds on LAN.
- NFR-3: Broker API should be stateless and horizontally scalable.
- NFR-4: Principle of least privilege for services and package scripts.
- NFR-5: Maintainability through modular code and explicit CLI contracts.

## 4. Constraints
- C-1: Initial release targets X11 desktops with `x11vnc`.
- C-2: Wayland support is deferred and planned via `wayvnc` adapter.
- C-3: NAT traversal relay is outside v1 scope; deployment assumes routable host or VPN.

## 5. Acceptance Criteria
- AC-1: `yourdesk broker` starts and serves health/API endpoints.
- AC-2: `yourdesk host` registers code and cleans up on termination.
- AC-3: `yourdesk join` resolves active code and prints viewer URL.
- AC-4: Packaging metadata exists for `.deb`, `.rpm`, and Arch package workflows.
