from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import RequireRole, get_db
from app.schemas.dance_class import DanceClassCreate, DanceClassResponse
from app.services import dance_class_service


router = APIRouter()


@router.post("/", response_model=DanceClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(
	class_in: DanceClassCreate,
	db: Session = Depends(get_db),
	school_id: int = Depends(RequireRole(["SCHOOL_ADMIN"])),
) -> DanceClassResponse:
	return dance_class_service.create_dance_class(db, class_in, school_id)
