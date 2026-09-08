import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.global_entities import User


bearer_scheme = HTTPBearer()


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def get_current_user(
	credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
	db: Session = Depends(get_db),
) -> User:
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)

	try:
		payload = jwt.decode(
			credentials.credentials,
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
