import uuid

from sqlalchemy import Column, Index, Integer, Text, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class UUID(types.TypeDecorator):
    impl = types.LargeBinary

    def __init__(self):
        self.impl.length = 16
        types.TypeDecorator.__init__(self, length=self.impl.length)

    def process_bind_param(self, value, dialect=None):
        if value and isinstance(value, uuid.UUID):
            return value.bytes
        elif value and isinstance(value, basestring):
            return uuid.UUID(value).bytes
        elif value:
            raise ValueError('value %s is not a valid uuid.UUId' % value)
        else:
            return None

    def process_result_value(self, value, dialect=None):
        if value:
            return uuid.UUID(bytes=value)
        else:
            return None

    def is_mutable(self):
        return False


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)


class Profile(Base):
    __tablename__ = 'profiles'
    uuid = Column('uuid', UUID(), primary_key=True, default=uuid.uuid4)
    title = Column(Text)
    num_messages_pre = Column(Integer)
    num_messages_post = Column(Integer)
    send_days = Column(Text)

    def to_dict(self):
        return {
            'uuid': str(self.uuid),
            'title': self.title,
            'num_messages_pre': self.num_messages_pre,
            'num_messages_post': self.num_messages_post,
            'send_days': [int(d) for d in self.send_days.split(',')],
        }
