from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; actor_user_id: int | None; actor_role: str | None; action: str; entity_type: str; entity_id: str | None; details: dict[str, object]; request_id: str | None; created_at: datetime
class AuditLogListResponse(BaseModel):
    items: list[AuditLogResponse]; total: int
class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; type: str; title: str; message: str; related_entity_type: str | None; related_entity_id: str | None; is_read: bool; created_at: datetime; read_at: datetime | None
class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]; total: int; unread_count: int
class InvoiceActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; invoice_id: int; event_type: str; title: str; description: str | None; actor_user_id: int | None; details: dict[str, object]; created_at: datetime
