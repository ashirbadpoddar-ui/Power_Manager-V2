export type Notification = { id: number; type: string; title: string; message: string; related_entity_type: string | null; related_entity_id: string | null; is_read: boolean; created_at: string; read_at: string | null };
export type NotificationList = { items: Notification[]; total: number; unread_count: number };
export type AuditLog = { id: number; actor_user_id: number | null; actor_role: string | null; action: string; entity_type: string; entity_id: string | null; details: Record<string, unknown>; request_id: string | null; created_at: string };
export type InvoiceActivity = { id: number; invoice_id: number; event_type: string; title: string; description: string | null; actor_user_id: number | null; details: Record<string, unknown>; created_at: string };
