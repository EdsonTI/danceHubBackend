from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
	email: EmailStr
	password: str
	first_name: str
	last_name: str


class UserLogin(BaseModel):
	email: EmailStr
	password: str


class UserResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	email: EmailStr
	first_name: str
	last_name: str
	is_active: bool


class TokenResponse(BaseModel):
	access_token: str
	token_type: str = "bearer"
