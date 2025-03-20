from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from shared.utils import generate_uuid, utc_timestamp


class TimeStampedBaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        sa.String(36), unique=True, default=generate_uuid, sort_order=-1, index=True
    )

    incr_id: Mapped[int] = mapped_column(
        sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
        primary_key=True,
        autoincrement=True,
        sort_order=-2,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=utc_timestamp,
        sort_order=9997,
    )

    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        default=utc_timestamp,
        onupdate=utc_timestamp,
        sort_order=9998,
    )
