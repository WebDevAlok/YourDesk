from __future__ import annotations

from datetime import datetime, timedelta, timezone
import secrets
from threading import RLock
from typing import Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, HttpUrl

from yourdesk.config import BrokerConfig


class SessionCreateRequest(BaseModel):
    alias: str = Field(min_length=1, max_length=64)
    viewer_url: HttpUrl


class SessionCreateResponse(BaseModel):
    code: str
    secret: str
    expires_at: datetime


class SessionLookupResponse(BaseModel):
    alias: str
    viewer_url: HttpUrl
    expires_at: datetime


class SessionRecord(BaseModel):
    alias: str
    viewer_url: HttpUrl
    secret: str
    expires_at: datetime


class SessionStore:
    def __init__(self, ttl_seconds: int) -> None:
        self._ttl = ttl_seconds
        self._records: Dict[str, SessionRecord] = {}
        self._lock = RLock()

    def _gc(self) -> None:
        now = datetime.now(timezone.utc)
        expired = [k for k, v in self._records.items() if v.expires_at <= now]
        for key in expired:
            self._records.pop(key, None)

    def create(self, alias: str, viewer_url: str) -> SessionCreateResponse:
        with self._lock:
            self._gc()
            code = f"{secrets.randbelow(1000):03d}-{secrets.randbelow(1000):03d}-{secrets.randbelow(1000):03d}"
            while code in self._records:
                code = f"{secrets.randbelow(1000):03d}-{secrets.randbelow(1000):03d}-{secrets.randbelow(1000):03d}"
            secret = secrets.token_urlsafe(24)
            expires = datetime.now(timezone.utc) + timedelta(seconds=self._ttl)
            self._records[code] = SessionRecord(alias=alias, viewer_url=viewer_url, secret=secret, expires_at=expires)
            return SessionCreateResponse(code=code, secret=secret, expires_at=expires)

    def revoke(self, code: str, secret: str) -> None:
        with self._lock:
            self._gc()
            record = self._records.get(code)
            if not record or not secrets.compare_digest(record.secret, secret):
                raise HTTPException(status_code=404, detail="session not found")
            self._records.pop(code, None)

    def lookup(self, code: str) -> SessionLookupResponse:
        with self._lock:
            self._gc()
            record = self._records.get(code)
            if not record:
                raise HTTPException(status_code=404, detail="invalid or expired code")
            return SessionLookupResponse(alias=record.alias, viewer_url=record.viewer_url, expires_at=record.expires_at)


def create_app(config: BrokerConfig | None = None) -> FastAPI:
    config = config or BrokerConfig()
    app = FastAPI(title="YourDesk Broker", version="1.0.0")
    store = SessionStore(ttl_seconds=config.token_ttl_seconds)

    @app.get("/healthz")
    def healthz() -> dict:
        return {"status": "ok"}

    @app.post("/api/v1/sessions", response_model=SessionCreateResponse)
    def create_session(payload: SessionCreateRequest) -> SessionCreateResponse:
        return store.create(payload.alias, str(payload.viewer_url))

    @app.get("/api/v1/sessions/{code}", response_model=SessionLookupResponse)
    def lookup_session(code: str) -> SessionLookupResponse:
        return store.lookup(code)

    @app.delete("/api/v1/sessions/{code}")
    def revoke_session(code: str, secret: str) -> dict:
        store.revoke(code, secret)
        return {"status": "revoked"}

    return app


app = create_app()
