from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
	from app.models.global_entities import User
	from app.models.tenant_entities import School


class DanceClass(Base):
	__tablename__ = "dance_classes"

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	school_id: Mapped[int] = mapped_column(
		ForeignKey("schools.id", ondelete="CASCADE")
	)
	name: Mapped[str] = mapped_column(String(150))
	description: Mapped[str | None] = mapped_column(String(500), nullable=True)
	level: Mapped[str] = mapped_column(String(50))
	max_capacity: Mapped[int] = mapped_column(Integer)
	visibility: Mapped[str] = mapped_column(String(50), default="PUBLIC")

	school: Mapped["School"] = relationship()
	enrollments: Mapped[list["ClassEnrollment"]] = relationship(
		back_populates="dance_class", cascade="all, delete-orphan"
	)


class ClassEnrollment(Base):
	__tablename__ = "class_enrollments"
	__table_args__ = (
		UniqueConstraint(
			"user_id",
			"dance_class_id",
			name="uix_class_enrollment_user_class",
		),
	)

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	school_id: Mapped[int] = mapped_column(
		ForeignKey("schools.id", ondelete="CASCADE")
	)
	dance_class_id: Mapped[int] = mapped_column(
		ForeignKey("dance_classes.id", ondelete="CASCADE")
	)
	user_id: Mapped[int] = mapped_column(
		ForeignKey("users.id", ondelete="CASCADE")
	)
	status: Mapped[str] = mapped_column(String(50), default="ACTIVE")

	school: Mapped["School"] = relationship()
	dance_class: Mapped["DanceClass"] = relationship(
		back_populates="enrollments"
	)
	user: Mapped["User"] = relationship()
