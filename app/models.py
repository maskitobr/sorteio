from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.types import Date, JSON
from sqlalchemy.orm import relationship
from .database import Base
import datetime


class Units(Base):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True, index=True,
                unique=True, nullable=False)
    num = Column(Integer)
    dual = Column(Boolean)
    spaces = relationship('Spaces', back_populates='owner')

    @property
    def serialize_spaces(self):
        """
        Return object's relations in easily serializable format.
        NB! Calls many2many's serialize property.
        """
        return [
            {
                "vaga": space.num,
                "tipo": ("Coberta" if space.covered else "Descoberta"),
                "piso": space.floor
            } for space in self.spaces
        ]

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "num": self.num,
            "spaces": self.serialize_spaces
        }


class Spaces(Base):
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

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "num": self.num,
            "floor": self.floor,
            "covered": ("Coberta" if self.covered else "Descoberta"),
            "reserved": self.reserved,
            "locked": self.locked,
            "owner": self.owner_id,
        }


class Results(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True, index=True,
                unique=True, nullable=False)
    year = Column(Integer)
    result = Column(JSON)
