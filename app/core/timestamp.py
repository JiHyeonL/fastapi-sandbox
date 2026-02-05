from datetime import datetime

from sqlalchemy import DateTime, event
from sqlalchemy.orm import declared_attr, Mapped, mapped_column


class BaseTimeEntity:
    """
    모든 모델(엔티티) created_at, updated_at 필드를 자동으로 추가한다.
    (SQLAlchemy Event Listeners 활용)

    - 엔티티 생성 시 create_at, updated_at 자동 추가
    - 엔티티 수정 시 updated_at 자동 갱신
    """

    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime,
            nullable=False,
            default=lambda : datetime.now(),
            comment="생성 일시"
        )

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime,
            nullable=False,
            default=lambda : datetime.now(),
            comment="수정 일시"
        )

@event.listens_for(BaseTimeEntity, 'before_insert', prpagate=True)
def before_insert_lister(target):
    now = datetime.now()
    if hasattr(target, 'created_at') and target.created_at is None:
        target.created_at = now
    if hasattr(target, 'updated_at') and target.updated_at is None:
        target.updated_at = now

@event.listens_for(BaseTimeEntity, 'before_update', propagate=True)
def before_update_lister(target):
    if hasattr(target, 'updated_at') and target.updated_at is None:
        target.updated_at = datetime.now()
