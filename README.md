# YourDesk

YourDesk is an AnyDesk-like remote support toolkit for Linux desktops. It provides:

- A **broker service** for session discovery and access control.
- A **host agent** that launches a local VNC stack (`x11vnc` + `noVNC`) and registers a one-time support code.
- A **join client** that resolves a support code and opens a secure viewer URL.

See `docs/` for full requirements, architecture, implementation plan, and user manual.
