"""Persisted, deliberately non-sensitive application activity."""
from __future__ import annotations
from typing import Any
from fastapi import Request
from sqlalchemy.orm import Session
from app.models.activity import AuditLog, InvoiceActivity, Notification
from app.models.user import User

_SENSITIVE = {"password", "password_hash", "token", "cookie", "secret", "api_key", "database_url", "authorization"}
def safe_details(value: Any) -> dict[str, object]:
    if not isinstance(value, dict): return {}
    def clean(item: Any) -> Any:
        if isinstance(item, dict): return {str(k): "[redacted]" if any(word in str(k).lower() for word in _SENSITIVE) else clean(v) for k, v in item.items()}
        if isinstance(item, (str, int, float, bool)) or item is None: return item
        if isinstance(item, (list, tuple)): return [clean(v) for v in item][:20]
        return str(item)
    return clean(value)
def record_audit(db: Session, *, actor: User | None, action: str, entity_type: str, entity_id: int | str | None, request: Request | None = None, details: dict[str, object] | None = None) -> None:
    db.add(AuditLog(actor_user_id=actor.id if actor else None, actor_role=actor.role if actor else None, action=action, entity_type=entity_type, entity_id=str(entity_id) if entity_id is not None else None, request_id=getattr(getattr(request, "state", None), "request_id", None), details=safe_details(details or {})))
def create_notification(db: Session, *, user_id: int, type: str, title: str, message: str, entity_type: str | None = None, entity_id: int | str | None = None) -> None:
    db.add(Notification(user_id=user_id, type=type, title=title, message=message, related_entity_type=entity_type, related_entity_id=str(entity_id) if entity_id is not None else None))
def record_invoice_activity(db: Session, *, invoice_id: int, event_type: str, title: str, actor: User | None = None, description: str | None = None, details: dict[str, object] | None = None) -> None:
    db.add(InvoiceActivity(invoice_id=invoice_id, event_type=event_type, title=title, description=description, actor_user_id=actor.id if actor else None, details=safe_details(details or {})))
