from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import RequireSuperAdmin, get_current_user, get_db
from app.models.global_entities import User
from app.schemas.tenant import (
	AssignRoleRequest,
	SchoolCreate,
	SchoolResponse,
	SchoolStatusUpdate,
)
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
	current_user: User = Depends(get_current_user)) -> SchoolResponse:
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


@router.patch(
	"/{school_id}/status",
	response_model=SchoolResponse,
)
def update_school_status(
	school_id: int,
	payload: SchoolStatusUpdate,
	db: Session = Depends(get_db),
	superadmin_id: int = Depends(RequireSuperAdmin),
) -> SchoolResponse:
	return school_service.update_school_status(db, school_id, payload.status)


@router.post("/{school_id}/assign-role")
def assign_role(
	school_id: int,
	payload: AssignRoleRequest,
	db: Session = Depends(get_db),
	superadmin_id: int = Depends(RequireSuperAdmin),
) -> dict[str, str]:
	try:
		return school_service.assign_role_to_school(db, school_id, payload)
	except ValueError as error:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=str(error),
		) from error