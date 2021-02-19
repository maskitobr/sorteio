from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.types import Date
from sqlalchemy.orm import relationship
from .database import Base
import datetime


class DictMixIn:
    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(
                getattr(self, column.name), (datetime.datetime, datetime.date)
            )
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }


class Units(Base, DictMixIn):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True, index=True,
                unique=True, nullable=False)
    num = Column(Integer)
    dual = Column(Boolean)
    spaces = relationship('Spaces', back_populates='owner')

    # def __repr__(self):
    #     return f'Units(num={self.num}, dual={self.dual}, spaces={self.spaces})'

    def __repr__(self):
        return f'num: {self.num} | spaces: {self.spaces}'


class Spaces(Base, DictMixIn):
    __tablename__ = 'spaces'

    id = Column(Integer, primary_key=True, index=True,
                unique=True, nullable=False)
    num = Column(Integer)
    floor = Column(String)
    covered = Column(Boolean)
    reserved = Column(Boolean)
    locked = Column(Boolean)
    owner = relationship('Units', back_populates='spaces')
    owner_id = Column(Integer, ForeignKey('units.id'))

    # def __repr__(self):
    #     return f'Spaces(num={self.num}, floor={self.floor}, covered={self.covered}, reserved={self.reserved}, locked={self.locked}, owner={self.owner})'

    def __repr__(self):
        return f'Number: {self.num} | {"Covered" if self.covered else "Uncovered"} | Owner: {self.owner_id}'
