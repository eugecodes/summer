import sqlalchemy as sqlalchemy
from sqlalchemy.ext import declarative
import sqlalchemy.orm as orm

session_maker = orm.sessionmaker(autoflush=True, autocommit=False)
DBSession = orm.scoped_session(session_maker)

class ReprBase(object):
    """
        Extend the base class
    """
    def __repr__(self):
        return "%s(%s)" % (
                 (self.__class__.__name__),
                 ', '.join(["%s=%r" % (key, getattr(self, key))
                            for key in sorted(self.__dict__.keys())
                            if not key.startswith('_')]))

DeclarativeBase = declarative.declarative_base(cls=ReprBase)
metadata = DeclarativeBase.metadata

def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    DBSession.configure(bind=engine)

# Import model modules here.
from .models import *
