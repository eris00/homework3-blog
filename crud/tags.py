from sqlalchemy import select
from models.tags import Tag
from sqlalchemy.orm import Session


def get_or_create_tags(db: Session, tag_names: list[str]) -> list[Tag]:
    unique_tag_names = list(set(tag_names))

    # Step 1: Retrieve existing Tags from the db
    existing_tags_query = select(Tag).where(Tag.name.in_(unique_tag_names))
    existing_tags = db.scalars(existing_tags_query).all()

    existing_tag_names = {tag.name for tag in existing_tags}

    # Step 2:  identifiy tag names to be created
    new_tag_names = set(unique_tag_names) - existing_tag_names
    new_tags = [Tag(name=name) for name in new_tag_names]  # list comprehension

    # new_tags = []
    # for name in new_tag_names:
    #     tag = Tag(name=name)
    #     new_tags.apend(tag)

    db.add_all(new_tags)
    return existing_tags + new_tags

from sqlalchemy.orm import Session
from sqlalchemy import func
from models.tags import Tag, post_tags


def list_tags(db: Session):
    tags_with_counts = (
        db.query(
            Tag.id,
            Tag.name,
            func.count(post_tags.c.post_id).label("posts_count")
        )
        .outerjoin(post_tags, Tag.id == post_tags.c.tag_id)
        .group_by(Tag.id, Tag.name)
        .all()
    )

    # Convert query results into a list of dictionaries
    return [
        {"id": tag.id, "name": tag.name, "posts_count": tag.posts_count}
        for tag in tags_with_counts
    ]
