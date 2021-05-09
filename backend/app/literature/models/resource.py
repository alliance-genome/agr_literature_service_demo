from datetime import datetime
import pytz

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from sqlalchemy.orm import relationship

from literature.database.base import Base


class Resource(Base):
    __versioned__ = {}
    __tablename__ = 'resources'

    resource_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    curie = Column(
        String(),
        unique=True,
        index=True,
        nullable=False
    )

    references = relationship(
        "Reference",
        back_populates="resource"
    )

    title = Column(
        String(),
        nullable=True
    )

#    titleSynonyms = relationship('ResourceTitleSynonym' , backref='resource', lazy=True)

    isoAbbreviation = Column(
        String(255),
        unique=True,
        nullable=True
    )

    medlineAbbreviation = Column(
        String(255),
        unique=False,
        nullable=True
    )

    copyrightDate = Column(
        DateTime
    )

    publisher = Column(
        String(255),
        unique=False,
        nullable=True
    )

    printISSN = Column(
        String(255),
        unique=False,
        nullable=True
    )

    onlineISSN = Column(
        String(255),
        unique=False,
        nullable=True
    )

    authors = relationship(
        'Author',
        back_populates='resource',
        cascade="all, delete, delete-orphan"
    )

    editors = relationship(
        'Editor',
        back_populates='resource',
        cascade="all, delete, delete-orphan"
    )

#    volumes = relationship('ResourceVolume' , backref='resource', lazy=True)
    pages = Column(
        Integer,
        unique=False,
        nullable=True
    )
    abstract = Column(
        String(255),
        unique=False,
        nullable=True
    )
    summary = Column(
        String(255),
        unique=False,
        nullable=True
    )
    #crossReferences
    dateUpdated = Column(
        DateTime,
        nullable=True,
    )
    dateCreated = Column(
        DateTime,
        nullable=False,
        default=datetime.now(tz=pytz.timezone('UTC'))
    )

