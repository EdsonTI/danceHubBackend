from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.global_entities import User
from app.models.tenant_entities import RoleAssignment
from app.schemas.identity import TokenResponse


def register_user(
	db: Session,
	email: str,
	password: str,
	first_name: str,
	last_name: str,
) -> User:
	existing_user = db.scalar(select(User).where(User.email == email))
	if existing_user is not None:
		raise ValueError("A user with this email already exists")

	user = User(
		email=email,
		hashed_password=get_password_hash(password),
		first_name=first_name,
		last_name=last_name,
	)
	db.add(user)

	try:
		db.commit()
	except IntegrityError:
		db.rollback()
		raise ValueError("A user with this email already exists") from None

	db.refresh(user)
	return user


def authenticate_user(
	db: Session,
	email: str,
	password: str,
) -> User | None:
	user = db.scalar(select(User).where(User.email == email))
	if user is None or not verify_password(password, user.hashed_password):
		return None

	return user


def switch_context(
	db: Session,
	user: User,
	school_id: int,
) -> TokenResponse:
	assignment = db.scalar(
		select(RoleAssignment)
		.options(joinedload(RoleAssignment.role))
		.where(
			RoleAssignment.user_id == user.id,
			RoleAssignment.school_id == school_id,
		)
	)
	if assignment is None or not assignment.is_active:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Acceso denegado a esta escuela",
		)

	access_token = create_access_token(
		{
			"sub": str(user.id),
			"active_school_id": school_id,
			"active_role": assignment.role.name,
		}
	)
	return TokenResponse(access_token=access_token)
