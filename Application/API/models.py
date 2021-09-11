from sqlalchemy import Boolean, Column, String, Integer, PickleType
from sqlalchemy.ext.mutable import MutableList

from Application.app import Base, engine, relationship, ForeignKey


class DBPeople(Base):

    __tablename__ = 'people'

    name = Column(String(50), primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    peoples_liked_by_me = Column(MutableList.as_mutable(PickleType), default=[])
    peoples_who_like_me = Column(MutableList.as_mutable(PickleType), default=[])
    likes = relationship("DBlikes")


class DBlikes(Base):

    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, index=True)
    from_user = Column(String(50))
    to_user = Column(String, ForeignKey('people.name'))


Base.metadata.create_all(bind=engine)
