import uuid

from sqlalchemy import Column, Index, Integer, Text, types, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship

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
    send_days = Column(Text)
    message_profiles = relationship("MessageProfile", backref="profile")

    def to_dict(self):
        return {
            'uuid': str(self.uuid),
            'title': self.title,
            'send_days': [int(d) for d in self.send_days.split(',')],
        }


class MessageProfile(Base):
    __tablename__ = 'message_profiles'
    uuid = Column('uuid', UUID(), primary_key=True, default=uuid.uuid4)
    name = Column(Text)
    profile_id = Column(Integer, ForeignKey('profiles.uuid'))
    messages = relationship('Message', backref='translation')


class Message(Base):
    __tablename__ = 'messages'
    uuid = Column('uuid', UUID(), primary_key=True, default=uuid.uuid4)
    message_profile_id = Column(Integer, ForeignKey('message_profiles.uuid'))
    week = Column(Integer)
    text = Column(Text)
