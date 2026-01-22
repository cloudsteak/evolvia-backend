from pydantic import BaseModel, EmailStr


class LabRequest(BaseModel):
    lab_name: str
    cloud_provider: str
    email: EmailStr
    lab_ttl: int


class LabReadyRequest(BaseModel):
    username: str
    status: str


class LabDeleteRequest(BaseModel):
    username: str


class VerifyLabRequest(BaseModel):
    user: str
    email: EmailStr
    cloud: str
    lab: str


status_map = {
    "ready": "success",
    "failed": "error",
}
