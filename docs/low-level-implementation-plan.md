# Low-Level Implementation Plan (LLD)

## Module Breakdown
- `yourdesk.broker`
  - `SessionStore`: thread-safe in-memory TTL map.
  - REST endpoints:
    - `POST /api/v1/sessions`
    - `GET /api/v1/sessions/{code}`
    - `DELETE /api/v1/sessions/{code}?secret=...`
- `yourdesk.cli`
  - `broker`: boot API service.
  - `host`: dependency checks, process supervision, registration/revocation.
  - `join`: session lookup for operator workflow.

## Implementation Steps
1. Build typed API models and store abstraction.
2. Add CLI parser with subcommands.
3. Implement host orchestration and graceful shutdown handlers.
4. Add tests for broker lifecycle and CLI parser behavior.
5. Add Linux package specs and systemd units.

## Justification for Key Decisions
- **In-memory session store (v1)**: no external DB required for single-node operations, lowers operational complexity.
- **Secret-based revocation**: avoids authenticated account system in MVP while preventing arbitrary deletion.
- **Process supervision inside host command**: deterministic cleanup and reduced stale registrations.
- **OS packaging specs included**: enables reproducible installation paths for multiple Linux families.

## Production Hardening Backlog
- Redis-backed session storage.
- Mutual TLS between host and broker.
- Wayland capture backend and hardware encode optimization.
- Native UI shell and auto-update channel.
