from pydantic import BaseModel

class ConfigResponse(BaseModel):
    id: int
    name: str
    folder: str
    s3_url: str

    class Config:
        orm_mode = True
