from sqlalchemy.orm import Session

from app.models.local_entities import DanceClass
from app.schemas.dance_class import DanceClassCreate


def create_dance_class(
	db: Session,
	class_in: DanceClassCreate,
	school_id: int,
) -> DanceClass:
	dance_class = DanceClass(
		name=class_in.name,
		description=class_in.description,
		level=class_in.level,
		max_capacity=class_in.max_capacity,
		visibility=class_in.visibility,
		school_id=school_id,
	)
	db.add(dance_class)
	db.commit()
	db.refresh(dance_class)
	return dance_class
