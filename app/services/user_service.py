from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.tenant_entities import RoleAssignment


def get_user_schools(db: Session, user_id: int) -> list[dict]:
	assignments = db.scalars(
		select(RoleAssignment)
		.options(
			joinedload(RoleAssignment.school),
			joinedload(RoleAssignment.role),
		)
		.where(RoleAssignment.user_id == user_id)
	).all()

	return [
		{"school": assignment.school, "role_name": assignment.role.name}
		for assignment in assignments
	]
