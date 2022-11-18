from datetime import datetime
from pydantic import BaseModel


class DataBase(BaseModel):
    image: str
    output: float

class DataCreate(DataBase):
    pass

class Data(DataBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class DataDelete(BaseModel):
    id_deleted: int

    class Config:
        orm_mode = True
