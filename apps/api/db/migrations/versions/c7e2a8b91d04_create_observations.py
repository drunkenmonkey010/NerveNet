"""create observations

Revision ID: c7e2a8b91d04
Revises: b01a4d3c2e7f
Create Date: 2026-08-23 14:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "c7e2a8b91d04"
down_revision: Union[str, Sequence[str], None] = "b01a4d3c2e7f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "observations",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("agent_id", sa.UUID(), nullable=False),
        sa.Column("observation_type", sa.String(length=100), nullable=False),
        sa.Column("subject_type", sa.String(length=100), nullable=True),
        sa.Column("subject_id", sa.UUID(), nullable=True),
        sa.Column("observed_value", postgresql.JSONB(), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("confidence", sa.Numeric(precision=5, scale=4), nullable=True),
        sa.Column("event_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "observed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
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
            "confidence IS NULL OR (confidence >= 0 AND confidence <= 1)",
            name="ck_observations_confidence_between_0_and_1",
        ),
        sa.ForeignKeyConstraint(
            ["agent_id"],
            ["agents.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_observations_agent_id"),
        "observations",
        ["agent_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_observations_event_time"),
        "observations",
        ["event_time"],
        unique=False,
    )
    op.create_index(
        op.f("ix_observations_observation_type"),
        "observations",
        ["observation_type"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_observations_observation_type"),
        table_name="observations",
    )
    op.drop_index(op.f("ix_observations_event_time"), table_name="observations")
    op.drop_index(op.f("ix_observations_agent_id"), table_name="observations")
    op.drop_table("observations")
