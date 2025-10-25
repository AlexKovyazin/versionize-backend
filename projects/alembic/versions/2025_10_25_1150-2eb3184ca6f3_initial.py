"""initial

Revision ID: 2eb3184ca6f3
Revises: 
Create Date: 2025-10-25 11:50:36.200899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2eb3184ca6f3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('default_sections',

    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('project_type', sa.Enum('LINEAR', 'AREAL', name='projecttypes'), nullable=False, comment='Тип объекта'),
    sa.Column('name', sa.String(), nullable=False, comment='Наименование раздела'),
    sa.Column('abbreviation', sa.String(), nullable=False, comment='Аббревиатура раздела'),

    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('project_type', 'abbreviation', name='uq_project_type_abbreviation'),
    sa.UniqueConstraint('project_type', 'name', name='uq_project_type_name')
    )
    op.create_index(op.f('ix_default_sections_created_at'), 'default_sections', ['created_at'], unique=False)
    op.create_index(op.f('ix_default_sections_id'), 'default_sections', ['id'], unique=False)
    op.create_index(op.f('ix_default_sections_project_type'), 'default_sections', ['project_type'], unique=False)

    op.create_table('projects',

    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('code', sa.String(), nullable=False, comment='Шифр'),
    sa.Column('name', sa.String(), nullable=False, comment='Наименование объекта'),
    sa.Column('exp_date', sa.DateTime(), nullable=True, comment='Срок экспертизы'),
    sa.Column('next_upload', sa.DateTime(), nullable=True, comment='Крайний срок следующей загрузки в экспертизу'),
    sa.Column('pm_id', sa.Uuid(), nullable=False, comment='ГИП'),
    sa.Column('project_type', sa.Enum('LINEAR', 'AREAL', name='projecttypes'), nullable=False, comment='Тип объекта'),
    sa.Column('company_id', sa.Uuid(), nullable=False, comment='Проектная организация'),

    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('company_id', 'code', name='uq_company_code'),
    sa.UniqueConstraint('company_id', 'name', name='uq_company_name')
    )
    op.create_index(op.f('ix_projects_code'), 'projects', ['code'], unique=False)
    op.create_index(op.f('ix_projects_created_at'), 'projects', ['created_at'], unique=False)
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)

    op.create_table('sections',

    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(), nullable=False, comment='Наименование раздела'),
    sa.Column('abbreviation', sa.String(), nullable=False, comment='Аббревиатура раздела'),
    sa.Column('project_id', sa.Uuid(), nullable=False, comment='Объект'),
    sa.Column('company_id', sa.Uuid(), nullable=False, comment='Ответственная организация'),
    sa.Column('responsible_id', sa.Uuid(), nullable=False, comment='Ответственный исполнитель'),
    sa.Column('expert_id', sa.Uuid(), nullable=False, comment='Эксперт'),

    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('project_id', 'abbreviation', name='uq_project_abbreviation'),
    sa.UniqueConstraint('project_id', 'name', name='uq_project_name')
    )
    op.create_index(op.f('ix_sections_company_id'), 'sections', ['company_id'], unique=False)
    op.create_index(op.f('ix_sections_created_at'), 'sections', ['created_at'], unique=False)
    op.create_index(op.f('ix_sections_expert_id'), 'sections', ['expert_id'], unique=False)
    op.create_index(op.f('ix_sections_id'), 'sections', ['id'], unique=False)
    op.create_index(op.f('ix_sections_project_id'), 'sections', ['project_id'], unique=False)
    op.create_index(op.f('ix_sections_responsible_id'), 'sections', ['responsible_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_sections_responsible_id'), table_name='sections')
    op.drop_index(op.f('ix_sections_project_id'), table_name='sections')
    op.drop_index(op.f('ix_sections_id'), table_name='sections')
    op.drop_index(op.f('ix_sections_expert_id'), table_name='sections')
    op.drop_index(op.f('ix_sections_created_at'), table_name='sections')
    op.drop_index(op.f('ix_sections_company_id'), table_name='sections')
    op.drop_table('sections')
    op.drop_index(op.f('ix_projects_id'), table_name='projects')
    op.drop_index(op.f('ix_projects_created_at'), table_name='projects')
    op.drop_index(op.f('ix_projects_code'), table_name='projects')
    op.drop_table('projects')
    op.drop_index(op.f('ix_default_sections_project_type'), table_name='default_sections')
    op.drop_index(op.f('ix_default_sections_id'), table_name='default_sections')
    op.drop_index(op.f('ix_default_sections_created_at'), table_name='default_sections')
    op.drop_table('default_sections')
    op.execute('DROP TYPE IF EXISTS projecttypes')
    # ### end Alembic commands ###
