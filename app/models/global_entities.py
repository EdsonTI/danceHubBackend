from sqlalchemy import String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy import String, Boolean, ForeignKey, UniqueConstraint, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class User(Base):
    """La identidad base (El humano)"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relación: Un humano puede tener múltiples perfiles (ej. Profesor y Alumno)
    profiles: Mapped[list["UserProfile"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Role(Base):
    """El catálogo de roles posibles en DanceHub"""
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True) # SUPERADMIN, SCHOOL_ADMIN, TEACHER, STUDENT
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relación inversa
    profiles: Mapped[list["UserProfile"]] = relationship(back_populates="role")


class UserProfile(Base):
    """
    Los detalles adicionales del usuario según su rol (Global).
    Ejemplo: Si role_id es TEACHER, extra_details tendrá {"bio": "...", "instagram": "..."}
    """
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))
    
    # El campo mágico donde guardaremos todo sin tener que alterar la base de datos
    extra_details: Mapped[dict] = mapped_column(JSON, default={}, server_default='{}')

    # Restricción: Un usuario solo puede tener UN perfil por cada tipo de rol (Un solo perfil de profesor)
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uix_user_role_profile"),
    )

    # Relaciones
    user: Mapped["User"] = relationship(back_populates="profiles")
    role: Mapped["Role"] = relationship(back_populates="profiles")