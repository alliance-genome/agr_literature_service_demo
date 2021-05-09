from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy_continuum import make_versioned

from literature.database.base import Base
from literature.database.config import SQLALCHEMY_DATABASE_URL
from literature.continuum_plugins import  UserPlugin


metadata = MetaData()

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"options": "-c timezone=utc"})
Base.metadata.create_all(engine)

user_plugin = UserPlugin()

make_versioned(plugins=[user_plugin])
