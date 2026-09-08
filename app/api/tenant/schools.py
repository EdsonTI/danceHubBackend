from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.models.global_entities import User
from app.schemas.tenant import SchoolCreate, SchoolResponse
from app.services import school_service


router = APIRouter(tags=["Schools"])


@router.post(
	"/",
	response_model=SchoolResponse,
	status_code=status.HTTP_201_CREATED,
)
def create_school(
	school_in: SchoolCreate,
	db: Session = Depends(get_db),
	current_user: User = Depends(get_current_user),
) -> SchoolResponse:
	try:
		return school_service.create_school(
			db=db,
			school_in=school_in,
			current_user_id=current_user.id,
		)
	except ValueError as error:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=str(error),
		) from error