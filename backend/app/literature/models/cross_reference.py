from datetime import datetime
import pytz

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ARRAY

from sqlalchemy.orm import relationship

from literature.database.base import Base


class CrossReference(Base):
    __tablename__ = 'crossReferences'
    __versioned__ = {}

#    cross_reference_id = Column(
#        Integer,
#        primary_key=True,
#        autoincrement=True
#    )

    curie = Column(
        String,
        primary_key=True
    )

    reference_id = Column(
        Integer,
        ForeignKey('references.reference_id',
                   ondelete='CASCADE')
    )

    reference = relationship(
        'Reference',
        back_populates="crossReferences"
    )

    resource_id = Column(
        Integer,
        ForeignKey('resources.resource_id',
                   ondelete='CASCADE')
    )

    resource = relationship(
        'Resource',
        back_populates="crossReferences"
    )

    pages = Column(
       ARRAY(String()),
       nullable=True
    )
