from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.global_entities import Role


ROLE_NAMES = (
	"SUPERADMIN",
	"SCHOOL_ADMIN",
	"TEACHER",
	"STUDENT",
)


def init_roles() -> None:
	db = SessionLocal()
	try:
		for role_name in ROLE_NAMES:
			role = db.scalar(select(Role).where(Role.name == role_name))
			if role is None:
				db.add(Role(name=role_name))

		db.commit()
	except Exception:
		db.rollback()
		raise
	finally:
		db.close()


if __name__ == "__main__":
	init_roles()
