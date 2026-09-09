from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.models.global_entities import User
from app.schemas.user import UserSchoolRoleResponse
from app.services import user_service


router = APIRouter(tags=["Users"])


@router.get("/me/schools", response_model=list[UserSchoolRoleResponse])
def get_my_schools(
	db: Session = Depends(get_db),
	current_user: User = Depends(get_current_user),
) -> list[UserSchoolRoleResponse]:
	return user_service.get_user_schools(db, current_user.id)
