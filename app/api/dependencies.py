import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.global_entities import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/tenant/auth/login")


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def get_current_user(
	token: str = Depends(oauth2_scheme),
	db: Session = Depends(get_db),
) -> User:
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)

	try:
		payload = jwt.decode(
			token,
			settings.SECRET_KEY,
			algorithms=[settings.ALGORITHM],
		)
		subject = payload.get("sub")
		if subject is None:
			raise credentials_exception
		user_id = int(subject)
	except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
		raise credentials_exception from None

	user = db.get(User, user_id)
	if user is None:
		raise credentials_exception

	return user
