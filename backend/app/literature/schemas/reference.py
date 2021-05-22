from typing import List, Optional

from pydantic import BaseModel

from literature.schemas.base import BaseModelShow
from literature.schemas.author import AuthorSchemaPost
from literature.schemas.author import AuthorSchemaShow
from literature.schemas.editor import EditorSchemaPost
from literature.schemas.editor import EditorSchemaShow
from literature.schemas.resource import ResourceSchemaShow
from literature.schemas.reference_category import ReferenceCategory
from literature.schemas.mod_reference_type import ModReferenceType
from literature.schemas.reference_tag import ReferenceTag
from literature.schemas.mesh_detail import MeshDetail
from literature.schemas.mesh_detail import MeshDetailShow
from literature.schemas.cross_reference import CrossReferenceSchemaRelated


class ReferenceSchemaPost(BaseModel):
    title: str
    date_published: str
    category: ReferenceCategory
    citation: str

    date_arrived_in_pubmed: Optional[str] = None
    date_last_modified: Optional[str] = None
    volume: Optional[str] = None
    language: Optional[str] = None
    pages: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[List[str]] = None
    pubmed_type: Optional[List[str]] = None
    mod_reference_types: Optional[List[ModReferenceType]] = None
    publisher: Optional[str] = None
    issue_name: Optional[str] = None
    issue_date: Optional[str] = None
    tags: Optional[List[ReferenceTag]] = None
    mesh_terms: Optional[List[MeshDetail]] = None
    cross_references: Optional[List[CrossReferenceSchemaRelated]] = None
    authors: Optional[List[AuthorSchemaPost]] = None
    editors: Optional[List[EditorSchemaPost]] = None
    resource: Optional[str] = None

    class Config():
        orm_mode = True
        extra = "forbid"


class ReferenceSchemaUpdate(BaseModel):
    title: str
    date_published: str
    category: ReferenceCategory
    citation: str

    date_arrived_in_pubmed: Optional[str] = None
    date_last_modified: Optional[str] = None
    volume: Optional[str] = None
    language: Optional[str] = None
    pages: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[List[str]] = None
    pubmed_type: Optional[List[str]] = None
    mod_reference_types: Optional[List[ModReferenceType]] = None
    publisher: Optional[str] = None
    issue_name: Optional[str] = None
    issue_date: Optional[str] = None
    tags: Optional[List[ReferenceTag]] = None
    mesh_terms: Optional[List[MeshDetail]] = None
    cross_references: Optional[List[CrossReferenceSchemaRelated]] = None
    resource: Optional[str] = None

    class Config():
        orm_mode = True
        extra = "forbid"


class ReferenceSchemaShow(BaseModelShow):
    curie: str = None
    title: str
    date_published: str
    category: ReferenceCategory
    citation: str

    date_arrived_in_pubmed: Optional[str] = None
    date_last_modified: Optional[str] = None
    volume: Optional[str] = None
    language: Optional[str] = None
    pages: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[List[str]] = None
    pubmed_type: Optional[List[str]] = None
    mod_reference_types: Optional[List[ModReferenceType]] = None
    publisher: Optional[str] = None
    issue_name: Optional[str] = None
    issue_date: Optional[str] = None
    tags: Optional[List[ReferenceTag]] = None
    mesh_terms: Optional[List[MeshDetailShow]] = None
    cross_references: Optional[List[CrossReferenceSchemaRelated]] = None
    resource: Optional[ResourceSchemaShow] = None
    authors: Optional[List[AuthorSchemaShow]] = None
    editors: Optional[List[EditorSchemaShow]] = None

    class Config():
        orm_mode = True
        extra = "forbid"