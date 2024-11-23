from fastapi import APIRouter, Depends, HTTPException
from crud import tags
import crud.sections as sections
from exceptions import DbnotFoundException, SectionInUseError
from schemas.sections import Section, SectionCreate, SectionUpdate
from database import db
from schemas.tags import TagWithPostCount

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get("", response_model=list[TagWithPostCount])
def list_tags(db: db):
    return tags.list_tags(db)