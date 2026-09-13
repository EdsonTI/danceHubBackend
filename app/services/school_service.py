import re
import unicodedata

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.global_entities import Role, User
from app.models.tenant_entities import RoleAssignment, School
from app.schemas.tenant import AssignRoleRequest, SchoolCreate


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


def update_school_status(
	db: Session,
	target_school_id: int,
	new_status: str,
) -> School:
	school = db.get(School, target_school_id)
	if school is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Escuela no encontrada",
		)

	school.status = new_status
	if new_status == "ACTIVE":
		school.is_public = True
	elif new_status in {"REJECTED", "PENDING"}:
		school.is_public = False

	try:
		db.commit()
	except Exception:
		db.rollback()
		raise

	db.refresh(school)
	return school


def assign_role_to_school(
	db: Session,
	school_id: int,
	payload: AssignRoleRequest,
) -> dict[str, str]:
	school = db.get(School, school_id)
	if school is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Escuela no encontrada",
		)

	user = db.get(User, payload.user_id)
	if user is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Usuario no encontrado",
		)

	role = db.scalar(select(Role).where(Role.name == payload.role_name))
	if role is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Rol no encontrado",
		)

	existing_assignment = db.scalar(
		select(RoleAssignment).where(
			RoleAssignment.user_id == payload.user_id,
			RoleAssignment.role_id == role.id,
			RoleAssignment.school_id == school_id,
		)
	)
	if existing_assignment is not None:
		raise ValueError("El usuario ya tiene este rol en esta escuela")

	db.add(
		RoleAssignment(
			user_id=payload.user_id,
			school_id=school_id,
			role_id=role.id,
		)
	)

	try:
		db.commit()
	except Exception:
		db.rollback()
		raise

	return {"detail": "Rol asignado correctamente"}