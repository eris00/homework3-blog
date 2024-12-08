from fastapi import Depends
from sqlalchemy import select
from typing import Annotated
from database import get_db
from models.posts import Post
from models.tags import Tag
from sqlalchemy.orm import Session
from crud.tags import list_tags, delete_tag

def object_to_dict(obj):
    return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}


def delete_relatable_tags(db: Annotated[Session, Depends(get_db)], is_del_tags: bool, post_obj: Post):
    if is_del_tags:
        post_tags_list = list(post_obj.tags)
        post_tags = [object_to_dict(tag) for tag in post_tags_list]

        all_tags = list_tags(db)
        all_tags_dict = {tag["id"]: tag["posts_count"] for tag in all_tags}

        for tag in post_tags:
            tag_id = tag["id"]
            posts_counts = all_tags_dict.get(tag_id, 0) # 0 if there isn't posts

            if posts_counts == 0:
                delete_tag(db, tag_id)
                db.commit()




