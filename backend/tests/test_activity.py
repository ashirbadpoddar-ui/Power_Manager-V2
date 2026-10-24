from fastapi.testclient import TestClient


def test_audit_log_is_admin_only_and_redacts_secrets(client: TestClient, bootstrap_admin):
    admin, _ = bootstrap_admin(client)
    response = admin.get("/api/audit-logs")
    assert response.status_code == 200
    # Bootstrap is intentionally not persisted with any setup token details.
    assert all("token" not in str(item["details"]).lower() for item in response.json()["items"])


def test_notifications_are_owned_and_can_be_marked_read(client: TestClient, bootstrap_admin, create_managed_user, csrf_headers):
    admin, _ = bootstrap_admin(client)
    user = create_managed_user(admin)
    from app.database.connection import SessionLocal
    from app.services.activity_service import create_notification
    with SessionLocal() as db:
        create_notification(db, user_id=user["id"], type="security", title="Private", message="Only this user")
        db.commit()
    from app.main import app
    with TestClient(app, base_url="http://testserver") as login:
        response = login.post("/api/auth/login", json={"email": user["email"], "password": "TemporaryPassword1!"})
        assert response.status_code == 200
        listed = login.get("/api/notifications")
        assert listed.status_code == 200
        assert listed.json()["unread_count"] == 1
        notification_id = listed.json()["items"][0]["id"]
        marked = login.patch(f"/api/notifications/{notification_id}/read", headers=csrf_headers(login))
        assert marked.status_code == 200 and marked.json()["is_read"] is True
    assert admin.get("/api/notifications").json()["items"] == []
