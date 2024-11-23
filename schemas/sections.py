from pydantic import BaseModel, ConfigDict


class SectionBase(BaseModel):
    name: str  # TODO: min and max length must be defined!!


class SectionCreate(SectionBase):
    pass


class SectionUpdate(SectionBase):
    pass


class Section(SectionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
