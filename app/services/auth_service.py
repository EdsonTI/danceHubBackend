from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.global_entities import User


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
