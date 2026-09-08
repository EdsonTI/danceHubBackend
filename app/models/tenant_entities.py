from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.global_entities import Role, User


class School(Base):
    __tablename__ = "schools"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(50), default="PENDING", server_default="PENDING") # PENDING, APPROVED, REJECTED
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    role_assignments: Mapped[list["RoleAssignment"]] = relationship(
        back_populates="school", cascade="all, delete-orphan"
    )


class RoleAssignment(Base):
    __tablename__ = "role_assignments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id", ondelete="CASCADE"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Evita duplicar el mismo rol para el mismo usuario en la misma escuela
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", "school_id", name="uix_user_role_school"),
    )

    user: Mapped["User"] = relationship()
    role: Mapped["Role"] = relationship()
    school: Mapped["School"] = relationship(back_populates="role_assignments")