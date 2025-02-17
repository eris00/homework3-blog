from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, constr


class SectionBase(BaseModel):
    name: Annotated[str, Field(..., max_length=60, min_length=3)]


class SectionCreate(SectionBase):
    pass


class SectionUpdate(SectionBase):
    pass


class Section(SectionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)