from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field


class TagBase(BaseModel):
    name: Annotated[str, Field(..., max_length=25, min_length=2)] # tag can be abbreviation, like AI, CS, ML, ...


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class TagWithPostCount(Tag):
    posts_count: int