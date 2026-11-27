from alembic import op
import sqlalchemy as sa


revision = "0002_device_location"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("devices", sa.Column("location", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("devices", "location")