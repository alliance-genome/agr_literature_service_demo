from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import Response
from fastapi import Security

from fastapi_auth0 import Auth0User

from literature.schemas import ModReferenceTypeSchemaShow
from literature.schemas import ModReferenceTypeSchemaPost
from literature.schemas import ModReferenceTypeSchemaCreate
from literature.schemas import ModReferenceTypeSchemaUpdate

from literature.crud import mod_reference_type
from literature.routers.authentication import auth

router = APIRouter(
    prefix="/reference/mod_reference_type",
    tags=['Reference']
)


@router.post('/',
             status_code=status.HTTP_201_CREATED,
             response_model=ModReferenceTypeSchemaUpdate,
             dependencies=[Depends(auth.implicit_scheme)])
def create(request: ModReferenceTypeSchemaPost,
           user: Auth0User = Security(auth.get_user)):
    return mod_reference_type.create(request)


@router.delete('/{mod_reference_type_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(auth.implicit_scheme)])
def destroy(mod_reference_type_id: int,
            user: Auth0User = Security(auth.get_user)):
    mod_reference_type.destroy(mod_reference_type_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{mod_reference_type_id}',
            status_code=status.HTTP_202_ACCEPTED,
            response_model=ModReferenceTypeSchemaUpdate,
            dependencies=[Depends(auth.implicit_scheme)])
def update(mod_reference_type_id: int,
           request: ModReferenceTypeSchemaUpdate,
           user: Auth0User = Security(auth.get_user)):
    return mod_reference_type.update(mod_reference_type_id, request)


@router.get('/{mod_reference_type_id}',
            response_model=ModReferenceTypeSchemaUpdate,
            status_code=200)
def show(mod_reference_type_id: int):
    return mod_reference_type.show(mod_reference_type_id)


@router.get('/{mod_reference_type_id}/versions',
            status_code=200)
def show(mod_reference_type_id: int):
    return mod_reference_type.show_changesets(mod_reference_type_id)