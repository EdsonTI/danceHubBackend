from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.core.security import create_access_token
from app.schemas.identity import (
	TokenResponse,
	UserCreate,
	UserLogin,
	UserResponse,
)
from app.schemas.user import SwitchContextRequest
from app.models.global_entities import User
from app.services import auth_service


router = APIRouter(tags=["Authentication"])


@router.post(
	"/register",
	response_model=UserResponse,
	status_code=status.HTTP_201_CREATED,
)
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
	try:
		return auth_service.register_user(
			db=db,
			email=user_data.email,
			password=user_data.password,
			first_name=user_data.first_name,
			last_name=user_data.last_name,
		)
	except ValueError as error:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail=str(error),
		) from error


@router.post("/login", response_model=TokenResponse)
def login(
	user_data: UserLogin,
	db: Session = Depends(get_db),
) -> TokenResponse:
	user = auth_service.authenticate_user(
		db=db,
		email=user_data.email,
		password=user_data.password,
	)
	if user is None:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect email or password",
			headers={"WWW-Authenticate": "Bearer"},
		)

	access_token = create_access_token({"sub": str(user.id)})
	return TokenResponse(access_token=access_token)


@router.post("/switch", response_model=TokenResponse)
def switch_context(
	request: SwitchContextRequest,
	db: Session = Depends(get_db),
	current_user: User = Depends(get_current_user),
) -> TokenResponse:
	return auth_service.switch_context(db, current_user, request.school_id)
