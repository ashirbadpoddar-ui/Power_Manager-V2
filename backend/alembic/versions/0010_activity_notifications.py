"""Add persisted audit records, personal notifications, and invoice history.

Revision ID: 0010_activity
Revises: 0009_submitter_meter
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = "0010_activity"
down_revision = "0009_submitter_meter"
branch_labels = None
depends_on = None
def upgrade():
    op.create_table("audit_logs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("actor_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL")), sa.Column("actor_role", sa.String(32)), sa.Column("action", sa.String(80), nullable=False), sa.Column("entity_type", sa.String(64), nullable=False), sa.Column("entity_id", sa.String(64)), sa.Column("details", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")), sa.Column("request_id", sa.String(64)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("ix_audit_logs_created_at", "audit_logs", ["created_at"]); op.create_index("ix_audit_logs_action", "audit_logs", ["action"])
    op.create_table("notifications", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("type", sa.String(64), nullable=False), sa.Column("title", sa.String(160), nullable=False), sa.Column("message", sa.Text(), nullable=False), sa.Column("related_entity_type", sa.String(64)), sa.Column("related_entity_id", sa.String(64)), sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.text("false")), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()), sa.Column("read_at", sa.DateTime(timezone=True)))
    op.create_index("ix_notifications_user_created", "notifications", ["user_id", "created_at"]); op.create_index("ix_notifications_user_read", "notifications", ["user_id", "is_read"])
    op.create_table("invoice_activities", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("invoice_id", sa.Integer(), sa.ForeignKey("bills.id", ondelete="CASCADE"), nullable=False), sa.Column("event_type", sa.String(64), nullable=False), sa.Column("title", sa.String(160), nullable=False), sa.Column("description", sa.Text()), sa.Column("actor_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL")), sa.Column("details", postgresql.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("ix_invoice_activities_invoice_created", "invoice_activities", ["invoice_id", "created_at"])
def downgrade():
    op.drop_table("invoice_activities"); op.drop_table("notifications"); op.drop_table("audit_logs")
