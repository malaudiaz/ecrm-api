"""add publish_contract table

Revision ID: 9b6e921a034b
Revises: 8dee5cf2a01c
Create Date: 2024-06-28 14:04:30.972333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b6e921a034b'
down_revision: Union[str, None] = '8dee5cf2a01c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('publish_contracts',
    sa.Column('eid', sa.String(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.Unicode(length=24), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.Column('updated_by', sa.Unicode(length=24), nullable=False),
    sa.Column('service_name', sa.Unicode(length=12), nullable=False),
    sa.Column('publish_departament_eid', sa.String(), nullable=False),
    sa.Column('user_name', sa.Unicode(length=24), nullable=False),
    sa.Column('store_code', sa.Unicode(length=5), nullable=True),
    sa.Column('partner_address_eid', sa.Unicode(length=24), nullable=True),
    sa.Column('partner_address_type', sa.Unicode(length=30), nullable=True),
    sa.Column('contact_eid', sa.Unicode(length=24), nullable=True),
    sa.Column('campaign_eid', sa.String(), nullable=False),
    sa.Column('observation', sa.Unicode(length=250), nullable=True),
    sa.Column('initial_import', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.Column('publish_import', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.Column('discount_import', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.Column('total_import', sa.Numeric(precision=18, scale=2), nullable=True),
    sa.Column('initial_billing_eid', sa.Unicode(length=24), nullable=True),
    sa.Column('initial_billing_number', sa.Unicode(length=24), nullable=True),
    sa.Column('initial_payment_date', sa.DateTime(), nullable=True),
    sa.Column('initial_payment_system', sa.Unicode(length=30), nullable=True),
    sa.Column('publish_billing_eid', sa.Unicode(length=24), nullable=True),
    sa.Column('publish_billing_number', sa.Unicode(length=24), nullable=True),
    sa.Column('publish_billing_date', sa.DateTime(), nullable=True),
    sa.Column('publish_payment_date', sa.DateTime(), nullable=True),
    sa.Column('publish_payment_system', sa.Unicode(length=30), nullable=True),
    sa.Column('status', sa.Unicode(length=25), nullable=True),
    sa.ForeignKeyConstraint(['campaign_eid'], ['publishmgr.publish_campaign.eid'], ),
    sa.ForeignKeyConstraint(['publish_departament_eid'], ['publishmgr.publish_departament.eid'], ),
    sa.ForeignKeyConstraint(['user_name'], ['usermgr.users.user_name'], ),
    sa.PrimaryKeyConstraint('eid'),
    schema='publishmgr'
    )
    op.create_index(op.f('ix_publishmgr_publish_contracts_user_name'), 'publish_contracts', ['user_name'], unique=False, schema='publishmgr')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('publish_contracts', schema='publishmgr')
    # ### end Alembic commands ###
