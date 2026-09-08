import re
import unicodedata

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.global_entities import Role
from app.models.tenant_entities import RoleAssignment, School
from app.schemas.tenant import SchoolCreate


def _generate_slug(name: str) -> str:
	normalized_name = unicodedata.normalize("NFKD", name)
	ascii_name = normalized_name.encode("ascii", "ignore").decode("ascii")
	return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", ascii_name.lower())).strip("-")


def create_school(
	db: Session,
	school_in: SchoolCreate,
	current_user_id: int,
) -> School:
	if not school_in.accepted_terms:
		raise ValueError("Debes aceptar los términos contractuales")

	slug = school_in.slug.strip() if school_in.slug else ""
	school = School(
		name=school_in.name,
		slug=slug or _generate_slug(school_in.name),
		status="PENDING",
		is_public=False,
	)
	db.add(school)

	try:
		db.flush()

		rol_admin = db.scalar(select(Role).where(Role.name == "SCHOOL_ADMIN"))
		if rol_admin is None:
			raise ValueError("The SCHOOL_ADMIN role does not exist")

		db.add(
			RoleAssignment(
				user_id=current_user_id,
				school_id=school.id,
				role_id=rol_admin.id,
			)
		)
		db.commit()
	except Exception:
		db.rollback()
		raise

	db.refresh(school)
	return school