from pydantic import BaseModel, ConfigDict


class DanceClassBase(BaseModel):
	name: str
	description: str | None = None
	level: str
	max_capacity: int
	visibility: str = "PUBLIC"


class DanceClassCreate(DanceClassBase):
	pass


class DanceClassResponse(DanceClassBase):
	id: int
	school_id: int

	model_config = ConfigDict(from_attributes=True)


class ClassEnrollmentResponse(BaseModel):
	id: int
	dance_class_id: int
	user_id: int
	status: str

	model_config = ConfigDict(from_attributes=True)
