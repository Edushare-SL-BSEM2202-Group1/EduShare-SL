from pydantic import BaseModel
from typing import Optional

class ResourceBase(BaseModel):
    title: str
    description: Optional[str] = None

class ResourceCreate(ResourceBase):
    pass

class ResourceResponse(ResourceBase):
    id: int
    file_path: str

    class Config:
        from_attributes = True