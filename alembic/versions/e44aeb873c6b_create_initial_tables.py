"""create initial tables

Revision ID: e44aeb873c6b
Revises:
Create Date: 2026-02-12 05:51:23.917423+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e44aeb873c6b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tb_users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(254), unique=True, nullable=False, comment='이메일'),
        sa.Column('name', sa.String(100), nullable=True, comment='이름'),
        sa.Column('password_hash', sa.String(255), nullable=True, comment='해싱된 비밀번호'),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), comment='활성 여부 (소프트 삭제용)'),
        sa.Column('last_login', sa.DateTime(), nullable=True, comment='마지막 로그인 시간'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='생성 일시'),
        sa.Column('updated_at', sa.DateTime(), nullable=False, comment='수정 일시'),
    )

    op.create_table(
        'tb_user_profiles',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('tb_users.id', ondelete='CASCADE'), primary_key=True, comment='사용자 ID'),
        sa.Column('bio', sa.Text(), nullable=True, comment='자기소개'),
        sa.Column('avatar_url', sa.String(500), nullable=True, comment='아바타 URL'),
        sa.Column('phone', sa.String(20), nullable=True, comment='전화번호'),
        sa.Column('created_at', sa.DateTime(), nullable=False, comment='생성 일시'),
        sa.Column('updated_at', sa.DateTime(), nullable=False, comment='수정 일시'),
    )


def downgrade() -> None:
    op.drop_table('tb_user_profiles')
    op.drop_table('tb_users')
