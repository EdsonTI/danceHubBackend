from pydantic import BaseModel, ConfigDict

from app.schemas.tenant import SchoolResponse


class SwitchContextRequest(BaseModel):
	school_id: int


class UserSchoolRoleResponse(BaseModel):
	school: SchoolResponse
	role_name: str

	model_config = ConfigDict(from_attributes=True)
