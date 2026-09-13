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


class StudentInfo(BaseModel):
	id: int
	email: str
	first_name: str
	last_name: str

	model_config = ConfigDict(from_attributes=True)


class EnrollmentWithStudentResponse(BaseModel):
	id: int
	status: str
	user: StudentInfo

	model_config = ConfigDict(from_attributes=True)
