from typing import Literal

from pydantic import BaseModel, ConfigDict


class SchoolBase(BaseModel):
	name: str
	slug: str | None = None


class SchoolCreate(SchoolBase):
	accepted_terms: bool


class SchoolResponse(SchoolBase):
	id: int
	status: str
	is_public: bool
	is_active: bool

	model_config = ConfigDict(from_attributes=True)


class SchoolStatusUpdate(BaseModel):
	status: Literal["ACTIVE", "PENDING", "REJECTED"]


class AssignRoleRequest(BaseModel):
	user_id: int
	role_name: str = "SCHOOL_ADMIN"
