import { apiRequest } from "@/services/apiClient";
import type { AuditLog, InvoiceActivity, Notification, NotificationList } from "@/types/activity";
export const listNotifications = () => apiRequest<NotificationList>("/api/notifications?limit=20");
export const markNotificationRead = (id: number) => apiRequest<Notification>(`/api/notifications/${id}/read`, { method: "PATCH" });
export const markAllNotificationsRead = () => apiRequest<void>("/api/notifications/mark-all-read", { method: "POST" });
export const listAuditLogs = (offset = 0, search = "") => apiRequest<{ items: AuditLog[]; total: number }>(`/api/audit-logs?offset=${offset}&limit=30${search ? `&search=${encodeURIComponent(search)}` : ""}`);
export const getInvoiceActivity = (billId: number) => apiRequest<InvoiceActivity[]>(`/api/bills/${billId}/activity`);
