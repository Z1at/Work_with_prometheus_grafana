from pydantic import BaseModel


class HumanResponse(BaseModel):
    id: int
    name: str
    gender: str
    age: int

    class Config:
        from_attributes = True


class ListHumanResponse(BaseModel):
    lst: list[HumanResponse]


