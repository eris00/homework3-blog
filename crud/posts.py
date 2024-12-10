import os
from typing import Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import select
from crud.sections import get_section
from crud.tags import get_or_create_tags
from exceptions import DbnotFoundException
from models.posts import Post
from schemas.posts import FilterPosts, PostCreate, PostUpdate
from schemas.tags import Tag

UPLOAD_DIR = "public/images/posts/"

def get_post(db: Session, post_id: int) -> Post:
    post = db.get(Post, post_id)
    if not post:
        raise DbnotFoundException
    return post


def list_posts(db: Session, filters: Optional[FilterPosts] = None) -> list[Post]:
    query = select(Post)

    if filters:
        if filters.title:
            query = query.where(Post.title.ilike(f"%{filters.title}%"))

        if filters.section_id:
            query = query.where(Post.section_id == filters.section_id)

        if filters.tags:
            query = query.join(Post.tags).where(Tag.name.in_(filters.tags))

        if filters.created_at_gt:
            query = query.where(Post.created_at >= filters.created_at_gt)

        if filters.created_at_lt:
            query = query.where(Post.created_at <= filters.created_at_lt)

    return db.scalars(query).all()


def create_post(db: Session, post_data: PostCreate) -> Post:
    section = get_section(db, post_data.section_id)
    new_post = Post(**post_data.model_dump(exclude={"tags"}))
    new_post.section = section

    if post_data.tags:
        tags = get_or_create_tags(db, post_data.tags)
        new_post.tags = tags

    db.add(new_post)
    return new_post


def put_post(db: Session, post_id: int, post_data: PostCreate) -> Post:
    post_being_updated = get_post(db, post_id)

    update_data = post_data.model_dump(exclude_unset=True, exclude={"tags"})
    for key, value in update_data.items():
        setattr(post_being_updated, key, value)
    if post_data.tags:
        tags = get_or_create_tags(db, post_data.tags)
        post_being_updated.tags = tags

    return post_being_updated


def patch_post(db: Session, post_id: int, post_data: PostUpdate) -> Post:
    post_being_updated = get_post(db, post_id)

    update_data = post_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post_being_updated, key, value)

    if "tags" in update_data:
        tags = get_or_create_tags(db, update_data["tags"])
        post_being_updated.tags = tags

    return post_being_updated


def delete_post(db: Session, post_id: int) -> None:
    post = get_post(db, post_id)
    db.delete(post)

def upload_image(db: Session, post_id, image: UploadFile) -> Post:
    post = get_post(db, post_id)
    if not post:
        raise ValueError(f"Post with ID: {post_id} not found!")
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save the image
    image_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(image_path, "wb") as f:
        f.write(image.file.read())

    # Update the database with the image path
    post.image = image_path
    db.add(post)
    return post
    

    
