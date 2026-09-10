from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.global_entities import Role
from app.models.local_entities import ClassEnrollment, DanceClass
from app.models.tenant_entities import RoleAssignment, School


def enroll_user(
	db: Session,
	class_id: int,
	current_user_id: int,
) -> ClassEnrollment:
	try:
		dance_class = db.scalar(
			select(DanceClass)
			.join(School, DanceClass.school_id == School.id)
			.where(
				DanceClass.id == class_id,
				School.is_active.is_(True),
			)
		)
		if dance_class is None:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Clase no encontrada o inactiva",
			)

		active_enrollments = db.scalar(
			select(func.count(ClassEnrollment.id)).where(
				ClassEnrollment.dance_class_id == class_id,
				ClassEnrollment.status == "ACTIVE",
			)
		)
		if active_enrollments >= dance_class.max_capacity:
			raise ValueError("La clase está llena")

		existing_enrollment = db.scalar(
			select(ClassEnrollment).where(
				ClassEnrollment.dance_class_id == class_id,
				ClassEnrollment.user_id == current_user_id,
			)
		)
		if existing_enrollment is not None:
			raise ValueError("Ya estás matriculado")

		enrollment = ClassEnrollment(
			school_id=dance_class.school_id,
			dance_class_id=dance_class.id,
			user_id=current_user_id,
			status="ACTIVE",
		)
		db.add(enrollment)

		existing_role_assignment = db.scalar(
			select(RoleAssignment).where(
				RoleAssignment.user_id == current_user_id,
				RoleAssignment.school_id == dance_class.school_id,
			)
		)
		if existing_role_assignment is None:
			student_role = db.scalar(select(Role).where(Role.name == "STUDENT"))
			if student_role is None:
				raise ValueError("The STUDENT role does not exist")

			db.add(
				RoleAssignment(
					user_id=current_user_id,
					school_id=dance_class.school_id,
					role_id=student_role.id,
				)
			)

		db.commit()
	except Exception:
		db.rollback()
		raise

	db.refresh(enrollment)
	return enrollment
