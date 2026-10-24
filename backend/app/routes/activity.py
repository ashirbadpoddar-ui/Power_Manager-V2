from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select, update
from sqlalchemy.orm import Session
from app.api.dependencies import (
    get_current_user,
    require_administrator,
    require_csrf,
    require_operational_csrf_user,
    require_operational_user,
)
from app.database.connection import get_db
from app.models.activity import AuditLog, InvoiceActivity, Notification
from app.models.bill import Bill
from app.models.property import Submitter
from app.models.user import User
from app.schemas.activity import AuditLogListResponse, AuditLogResponse, InvoiceActivityResponse, NotificationListResponse, NotificationResponse

router = APIRouter(prefix="/api", tags=["activity"])

@router.get("/audit-logs", response_model=AuditLogListResponse)
def list_audit_logs(offset: int = Query(0, ge=0), limit: int = Query(30, ge=1, le=100), search: str | None = Query(None, max_length=100), action: str | None = Query(None, max_length=80), _: User = Depends(require_administrator), db: Session = Depends(get_db)):
    query = select(AuditLog)
    if action: query = query.where(AuditLog.action == action)
    if search:
        term = f"%{search.strip()}%"; query = query.where(or_(AuditLog.action.ilike(term), AuditLog.entity_type.ilike(term), AuditLog.entity_id.ilike(term)))
    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    items = db.scalars(query.order_by(AuditLog.created_at.desc(), AuditLog.id.desc()).offset(offset).limit(limit)).all()
    return AuditLogListResponse(items=[AuditLogResponse.model_validate(item) for item in items], total=total)

@router.get("/notifications", response_model=NotificationListResponse)
def list_notifications(offset: int = Query(0, ge=0), limit: int = Query(30, ge=1, le=100), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = select(Notification).where(Notification.user_id == user.id)
    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    unread = db.scalar(select(func.count()).select_from(Notification).where(Notification.user_id == user.id, Notification.is_read.is_(False))) or 0
    items = db.scalars(query.order_by(Notification.created_at.desc(), Notification.id.desc()).offset(offset).limit(limit)).all()
    return NotificationListResponse(items=[NotificationResponse.model_validate(item) for item in items], total=total, unread_count=unread)

@router.patch("/notifications/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(notification_id: int, user: User = Depends(require_csrf), db: Session = Depends(get_db)):
    item = db.scalar(select(Notification).where(Notification.id == notification_id, Notification.user_id == user.id).with_for_update())
    if item is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    if not item.is_read: item.is_read, item.read_at = True, datetime.now(timezone.utc); db.commit(); db.refresh(item)
    return NotificationResponse.model_validate(item)

@router.post("/notifications/mark-all-read", status_code=status.HTTP_204_NO_CONTENT)
def mark_all_notifications_read(user: User = Depends(require_csrf), db: Session = Depends(get_db)):
    db.execute(update(Notification).where(Notification.user_id == user.id, Notification.is_read.is_(False)).values(is_read=True, read_at=datetime.now(timezone.utc)))
    db.commit()

def _visible_invoice(db: Session, user: User, bill_id: int) -> Bill:
    query = select(Bill).where(Bill.id == bill_id)
    if user.role != "administrator":
        query = query.join(Submitter, Bill.submitter_id == Submitter.id).where(Submitter.user_id == user.id)
    bill = db.scalar(query)
    if bill is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return bill

@router.get("/bills/{bill_id}/activity", response_model=list[InvoiceActivityResponse])
def invoice_activity(bill_id: int, user: User = Depends(require_operational_user), db: Session = Depends(get_db)):
    _visible_invoice(db, user, bill_id)
    return [InvoiceActivityResponse.model_validate(item) for item in db.scalars(select(InvoiceActivity).where(InvoiceActivity.invoice_id == bill_id).order_by(InvoiceActivity.created_at.asc(), InvoiceActivity.id.asc())).all()]
