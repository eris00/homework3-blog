from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    name: str  # TODO: min and max length must be defined!!


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
