from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)


class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    num_messages_pre = Column(Integer)
    num_messages_post = Column(Integer)
    send_days = Column(Text)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'num_messages_pre': self.num_messages_pre,
            'num_messages_post': self.num_messages_post,
            'send_days': self.send_days,
        }
