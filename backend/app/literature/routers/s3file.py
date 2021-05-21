from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import Response
from fastapi import Security

from fastapi.responses import StreamingResponse

from botocore.client import BaseClient

from fastapi_auth0 import Auth0User

from literature.schemas import FileSchemaShow
from literature.schemas import FileSchemaUpdate

from literature.deps import s3_auth

from literature.crud import s3file
from literature.routers.authentication import auth


router = APIRouter(
    prefix="/file",
    tags=['File']
)


@router.delete('/{filename}',
               status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(auth.implicit_scheme)])
def destroy(filename: str,
            s3: BaseClient = Depends(s3_auth),
            user: Auth0User = Security(auth.get_user)):
    s3file.destroy(s3, filename)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{filename}',
            status_code=status.HTTP_202_ACCEPTED,
            response_model=FileSchemaShow,
            dependencies=[Depends(auth.implicit_scheme)])
def update(filename: str,
           request: FileSchemaUpdate,
           user: Auth0User = Security(auth.get_user)):
    return s3file.update(filename, request)


@router.get('/{filename}',
            response_model=FileSchemaShow,
            status_code=200)
def show(filename: str):
    return s3file.show(filename)


@router.get('/{filename}/download',
            status_code=200,
            dependencies=[Depends(auth.implicit_scheme)])
async def show(filename: str,
         s3: BaseClient = Depends(s3_auth),
         user: Auth0User = Security(auth.get_user)):
   [file_stream, media_type] = s3file.download(s3, filename)
   return StreamingResponse(file_stream, media_type=media_type)



@router.get('/{filename}/versions',
            status_code=200)
def show(filename: str):
    return s3file.show_changesets(filename)
