"""create memory events

Revision ID: d4f6b2a8c901
Revises: c7e2a8b91d04
Create Date: 2026-08-23 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "d4f6b2a8c901"
down_revision: Union[str, Sequence[str], None] = "c7e2a8b91d04"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "memory_events",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("agent_id", sa.UUID(), nullable=False),
        sa.Column("memory_type", sa.String(length=100), nullable=False),
        sa.Column("source_type", sa.String(length=100), nullable=True),
        sa.Column("source_id", sa.UUID(), nullable=True),
        sa.Column("content", postgresql.JSONB(), nullable=False),
        sa.Column("importance", sa.Numeric(precision=5, scale=4), nullable=True),
        sa.Column("event_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "importance IS NULL OR (importance >= 0 AND importance <= 1)",
            name="ck_memory_events_importance_between_0_and_1",
        ),
        sa.ForeignKeyConstraint(
            ["agent_id"],
            ["agents.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_memory_events_agent_id"),
        "memory_events",
        ["agent_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_memory_events_event_time"),
        "memory_events",
        ["event_time"],
        unique=False,
    )
    op.create_index(
        op.f("ix_memory_events_memory_type"),
        "memory_events",
        ["memory_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_memory_events_source_id"),
        "memory_events",
        ["source_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_memory_events_source_type"),
        "memory_events",
        ["source_type"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_memory_events_source_type"), table_name="memory_events")
    op.drop_index(op.f("ix_memory_events_source_id"), table_name="memory_events")
    op.drop_index(op.f("ix_memory_events_memory_type"), table_name="memory_events")
    op.drop_index(op.f("ix_memory_events_event_time"), table_name="memory_events")
    op.drop_index(op.f("ix_memory_events_agent_id"), table_name="memory_events")
    op.drop_table("memory_events")
