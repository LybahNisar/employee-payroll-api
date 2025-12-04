"""add salary columns

Revision ID: b4852be88c5f
Revises: 3d0074b5feab
Create Date: 2025-12-03 15:02:57.865302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4852be88c5f'
down_revision: Union[str, None] = '3d0074b5feab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Step 1: Add new columns as NULLABLE first (avoid errors on existing rows)
    op.add_column('staff', sa.Column('basic_salary', sa.Float(), nullable=True))
    op.add_column('staff', sa.Column('bonus_percentage', sa.Float(), nullable=True))

    # Step 2: Fill initial default values for existing rows
    op.execute("UPDATE staff SET basic_salary = 0 WHERE basic_salary IS NULL;")
    op.execute("UPDATE staff SET bonus_percentage = 0 WHERE bonus_percentage IS NULL;")

    # Step 3: Now enforce NOT NULL after populating data
    op.alter_column('staff', 'basic_salary', nullable=False)
    op.alter_column('staff', 'bonus_percentage', nullable=False)

    # Step 4: Change existing nullable fields to NOT NULL (safe)
    op.alter_column('staff', 'name', existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column('staff', 'age', existing_type=sa.INTEGER(), nullable=False)

    # Step 5: Remove old salary column
    op.drop_column('staff', 'salary')


def downgrade() -> None:
    # Recreate old salary column (NULL allowed)
    op.add_column('staff', sa.Column('salary', sa.DOUBLE_PRECISION(precision=53), nullable=True))

    # Revert NOT NULL constraints
    op.alter_column('staff', 'age', existing_type=sa.INTEGER(), nullable=True)
    op.alter_column('staff', 'name', existing_type=sa.VARCHAR(), nullable=True)

    # Drop the new columns
    op.drop_column('staff', 'bonus_percentage')
    op.drop_column('staff', 'basic_salary')
