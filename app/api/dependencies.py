import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.global_entities import User


oauth2_scheme = HTTPBearer()


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def get_current_user(
	credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
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


class RequireRole:
	def __init__(self, allowed_roles: list[str]):
		self.allowed_roles = allowed_roles

	def __call__(
		self,
		credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
	) -> int:
		try:
			payload = jwt.decode(
				credentials.credentials,
				settings.SECRET_KEY,
				algorithms=[settings.ALGORITHM],
			)
		except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Could not validate credentials",
				headers={"WWW-Authenticate": "Bearer"},
			) from None

		active_school_id = payload.get("active_school_id")
		active_role = payload.get("active_role")
		if active_school_id is None or active_role is None:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Debes seleccionar una escuela primero",
			)

		if active_role not in self.allowed_roles:
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail="No tienes permisos suficientes en esta escuela",
			)

		try:
			return int(active_school_id)
		except (TypeError, ValueError):
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Debes seleccionar una escuela primero",
			) from None


class RequireSuperAdmin:
	def __call__(
		self,
		credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
	) -> int:
		try:
			payload = jwt.decode(
				credentials.credentials,
				settings.SECRET_KEY,
				algorithms=[settings.ALGORITHM],
			)
		except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Could not validate credentials",
				headers={"WWW-Authenticate": "Bearer"},
			) from None

		if payload.get("is_superadmin") is not True:
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
				detail="Acceso denegado: Se requieren permisos de SuperAdmin",
			)

		try:
			return int(payload.get("sub"))
		except (TypeError, ValueError):
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Could not validate credentials",
				headers={"WWW-Authenticate": "Bearer"},
			) from None
