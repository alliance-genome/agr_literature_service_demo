from datetime import datetime
import pytz

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ARRAY

from sqlalchemy.orm import relationship

from literature.database.base import Base


class ResourceDescriptorPage(Base):
    __tablename__ = 'resource_descriptor_pages'

    resource_descriptor_pages_id = Column(
       Integer,
       primary_key=True,
       autoincrement=True
    )

    name = Column(
       String,
       unique=False,
       nullable=False
    )

    url = Column(
        String,
        unique=False,
        nullable=False
    )

    resource_descriptor_id = Column(
         Integer,
         ForeignKey('resource_descriptors.resource_descriptor_id',
                    ondelete='CASCADE')
    )

    resource_descriptor = relationship(
        'ResourceDescriptor',
        back_populates="pages"
    )




class ResourceDescriptor(Base):
    __tablename__ = 'resource_descriptors'

    resource_descriptor_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    pages = relationship(
        'ResourceDescriptorPage',
        lazy='joined',
        back_populates='resource_descriptor',
        cascade="all, delete, delete-orphan"
    )

    db_prefix = Column(
        String,
        nullable=False,
        unique=True
    )

    name = Column(
        String(),
        unique=False,
        nullable=True
    )

    aliases = Column(
        ARRAY(String()),
        nullable=True
    )

    example_gid = Column(
        String,
        nullable=True
    )

    gid_pattern = Column(
        String,
        nullable=True
    )

    default_url = Column(
        String(),
        unique=False,
        nullable=True
    )
