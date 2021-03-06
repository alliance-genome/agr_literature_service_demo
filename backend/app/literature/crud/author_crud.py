import sqlalchemy
from sqlalchemy.orm import Session
from datetime import datetime

from fastapi import HTTPException
from fastapi import status
from fastapi.encoders import jsonable_encoder

from literature.schemas import AuthorSchemaPost

from literature.models import ReferenceModel
from literature.models import ResourceModel
from literature.models import AuthorModel


def create(db: Session, author: AuthorSchemaPost):
    author_data = jsonable_encoder(author)

    if 'resource_curie' in author_data:
        resource_curie = author_data['resource_curie']
        del author_data['resource_curie']

    if 'reference_curie' in author_data:
        reference_curie = author_data['reference_curie']
        del author_data['reference_curie']

    if 'orchid' in author_data:
        orcid = author_data['orcid']
        del author_data['orcid']


    db_obj = AuthorModel(**author_data)
    if resource_curie and reference_curie:
       raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                           detail=f"Only supply either resource_curie or reference_curie")
    elif resource_curie:
       resource = db.query(ResourceModel).filter(ResourceModel.curie == resource_curie).first()
       if not resource:
           raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                               detail=f"Resource with curie {resource_curie} does not exist")
       db_obj.resource = resource
    elif reference_curie:
       reference = db.query(ReferenceModel).filter(ReferenceModel.curie == reference_curie).first()
       if not reference:
           raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                               detail=f"Reference with curie {reference_curie} does not exist")
       db_obj.reference = reference
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Supply one of resource_curie or reference_curie")

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return db_obj.author_id


def destroy(db: Session, author_id: int):
    author = db.query(AuthorModel).filter(AuthorModel.author_id == author_id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Author with author_id {author_id} not found")
    db.delete(author)
    db.commit()

    return None


def patch(db: Session, author_id: int, author_update: AuthorSchemaPost):

    author_db_obj = db.query(AuthorModel).filter(AuthorModel.author_id == author_id).first()
    if not author_db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Author with author_id {author_id} not found")


    if author_update.resource_curie and author_update.reference_curie:
       raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                           detail=f"Only supply either resource_curie or reference_curie")

    for field, value in author_update.items():
        if field == "resource_curie" and value:
            resource_curie = value
            resource = db.query(ResourceModel).filter(ResourceModel.curie == resource_curie).first()
            if not resource:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                  detail=f"Resource with curie {resource_curie} does not exist")
            author_db_obj.resource = resource
            author_db_obj.reference = None
        elif field == 'reference_curie' and value:
            reference_curie = value
            reference = db.query(ReferenceModel).filter(ReferenceModel.curie == reference_curie).first()
            if not reference:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                  detail=f"Reference with curie {reference_curie} does not exist")
            author_db_obj.reference = reference
            author_db_obj.resource = None
        else:
            setattr(author_db_obj, field, value)

    author_db_obj.dateUpdated = datetime.utcnow()
    db.commit()

    return "Updated"


def show(db: Session, author_id: int):
    author = db.query(AuthorModel).filter(AuthorModel.author_id == author_id).first()
    author_data = jsonable_encoder(author)

    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Author with the author_id {author_id} is not available")

    if author_data['resource_id']:
        author_data['resource_curie'] = db.query(Resource.curie).filter(Resource.resource_id == author_data['resource_id']).first()[0]
    del author_data['resource_id']

    if author_data['reference_id']:
        author_data['reference_curie'] = db.query(ReferenceModel.curie).filter(ReferenceModel.reference_id == author_data['reference_id']).first()[0]
    del author_data['reference_id']

    return author_data


def show_changesets(db: Session, author_id: int):
    author = db.query(AuthorModel).filter(AuthorModel.author_id == author_id).first()
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Author with the author_id {author_id} is not available")

    history = []
    for version in author.versions:
        tx = version.transaction
        history.append({'transaction': {'id': tx.id,
                                        'issued_at': tx.issued_at,
                                        'user_id': tx.user_id},
                        'changeset': version.changeset})

    return history
