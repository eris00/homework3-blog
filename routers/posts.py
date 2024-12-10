from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
import crud.posts as posts
from exceptions import DbnotFoundException
from schemas.posts import FilterPosts, Post, PostCreate, PostUpdate
from models.posts import Post as PostModel
from models.tags import Tag
from database import get_db
from sqlalchemy.orm import Session
from utils.auth import oauth2_scheme
from utils.background_tasks import delete_relatable_tags

router = APIRouter(prefix="/posts", tags=["posts"], dependencies=[Depends(oauth2_scheme)]) 

@router.get("", response_model=list[Post])
def list_posts(filters: Annotated[FilterPosts, Query()], db: Annotated[Session, Depends(get_db)]):
    return posts.list_posts(db, filters)


@router.get("/{post_id}", response_model=Post)
def get_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    try:
        return posts.get_post(db, post_id)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found!")


@router.post("", response_model=Post, status_code=201)
def create_post(post: PostCreate, db: Annotated[Session, Depends(get_db)]):
    post = posts.create_post(db, post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/{post_id}", response_model=Post)
def put_post(post_id: int, post: PostCreate, db: Annotated[Session, Depends(get_db)]):
    try:
        post = posts.put_post(db, post_id, post)
        db.commit()
        db.refresh(post)
        return post
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found!")
    

@router.patch("/{post_id}", response_model=Post)
def patch_post(post_id: int, post: PostUpdate, db: Annotated[Session, Depends(get_db)]):
    try:
        post = posts.patch_post(db, post_id, post)
        db.commit()
        db.refresh(post)
        return post
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found!")


@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int, db: Annotated[Session, Depends(get_db)],  background_tasks: BackgroundTasks, is_del_tags: bool = Query(...)):
    try:
        post_obj = db.get(PostModel, post_id)
        posts.delete_post(db, post_id)  
        db.commit()
        background_tasks.add_task(delete_relatable_tags, db, is_del_tags, post_obj)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found!")
