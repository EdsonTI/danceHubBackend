from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import RequireRole, get_current_user, get_db
from app.models.global_entities import User
from app.schemas.dance_class import (
	ClassEnrollmentResponse,
	DanceClassCreate,
	DanceClassResponse,
	EnrollmentWithStudentResponse,
)
from app.services import dance_class_service, enrollment_service


router = APIRouter()


@router.post("/", response_model=DanceClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(
	class_in: DanceClassCreate,
	db: Session = Depends(get_db),
	school_id: int = Depends(RequireRole(["SCHOOL_ADMIN"])),
) -> DanceClassResponse:
	return dance_class_service.create_dance_class(db, class_in, school_id)


@router.get("/{class_id}/students", response_model=list[EnrollmentWithStudentResponse])
def get_class_students(
	class_id: int,
	db: Session = Depends(get_db),
	school_id: int = Depends(RequireRole(["SCHOOL_ADMIN", "TEACHER"])),
) -> list[EnrollmentWithStudentResponse]:
	return enrollment_service.get_class_students(db, class_id, school_id)


@router.post(
	"/{class_id}/enroll",
	response_model=ClassEnrollmentResponse,
	status_code=status.HTTP_201_CREATED,
)
def enroll_in_class(
	class_id: int,
	db: Session = Depends(get_db),
	current_user: User = Depends(get_current_user),
) -> ClassEnrollmentResponse:
	try:
		return enrollment_service.enroll_user(db, class_id, current_user.id)
	except ValueError as error:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=str(error),
		) from error
