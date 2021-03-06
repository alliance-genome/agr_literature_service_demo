from typing import List

from sqlalchemy.orm import Session

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import Response
from fastapi import Security

from fastapi_auth0 import Auth0User

from literature import database

from literature.user import set_global_user_id
from literature.user import get_global_user_id

from literature.schemas import ResourceSchemaShow
from literature.schemas import ResourceSchemaPost
from literature.schemas import ResourceSchemaUpdate

from literature.schemas import NoteSchemaShow

from literature.crud import resource_crud

from literature.routers.authentication import auth


router = APIRouter(
    prefix="/resource",
    tags=['Resource']
)


get_db = database.get_db


@router.post('/',
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(auth.implicit_scheme)],
             response_model=str)
def create(request: ResourceSchemaPost,
           user: Auth0User = Security(auth.get_user),
           db: Session = Depends(get_db)):
    set_global_user_id(db, user.id)
    return resource_crud.create(db, request)


@router.delete('/{curie}',
               dependencies=[Depends(auth.implicit_scheme)],
               status_code=status.HTTP_204_NO_CONTENT)
def destroy(curie: str,
            user: Auth0User = Security(auth.get_user),
            db: Session = Depends(get_db)):
    set_global_user_id(db, user.id)
    resource_crud.destroy(db, curie)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/{curie}',
              status_code=status.HTTP_202_ACCEPTED,
              dependencies=[Depends(auth.implicit_scheme)],
              response_model=str)
def patch(curie: str,
          request: ResourceSchemaUpdate,
          user: Auth0User = Security(auth.get_user),
          db: Session = Depends(get_db)):
    set_global_user_id(db, user.id)
    patch = request.dict(exclude_unset=True)

    return resource_crud.patch(db, curie, patch)


@router.get('/{curie}/notes',
            status_code=200,
            response_model=List[NoteSchemaShow])
def show(curie: str,
         db: Session = Depends(get_db)):
     return resource_crud.show_notes(db, curie)


@router.get('/{curie}',
            status_code=200,
            response_model=ResourceSchemaShow)
def show(curie: str,
         db: Session = Depends(get_db)):
    print(curie)
    return resource_crud.show(db, curie)


@router.get('/{curie}/versions',
            status_code=200)
def show(curie: str,
         db: Session = Depends(get_db)):
    return resource_crud.show_changesets(db, curie)
