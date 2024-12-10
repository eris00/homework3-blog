from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from crud import tags
import crud.sections as sections
from exceptions import DbnotFoundException, SectionInUseError
from schemas.sections import Section, SectionCreate, SectionUpdate
from database import get_db
from schemas.tags import TagWithPostCount
from sqlalchemy.orm import Session
from utils.auth import oauth2_scheme


router = APIRouter(prefix="/tags", tags=["tags"], dependencies=[Depends(oauth2_scheme)])

@router.get("", response_model=list[TagWithPostCount])
def list_tags(db: Annotated[Session, Depends(get_db)]):
    return tags.list_tags(db)