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
    slots = relationship('Slots', back_populates='owner')

    @property
    def serialize_slots(self):
        """
        Return object's relations in easily serializable format.
        NB! Calls many2many's serialize property.
        """
        return [
            {
                "vaga": slot.num,
                "tipo": ("Coberta" if slot.covered else "Descoberta"),
                "piso": slot.floor
            } for slot in self.slots
        ]

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "num": self.num,
            "slots": self.serialize_slots
        }


class Slots(Base):
    __tablename__ = 'slots'

    id = Column(Integer, primary_key=True, index=True,
                unique=True, nullable=False)
    num = Column(Integer)
    floor = Column(String)
    covered = Column(Boolean)
    reserved = Column(Boolean)
    double = Column(Boolean)
    owner = relationship('Units', back_populates='slots')
    owner_id = Column(Integer, ForeignKey('units.id'))

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "num": self.num,
            "floor": self.floor,
            "covered": ("Coberta" if self.covered else "Descoberta"),
            "reserved": self.reserved,
            "double": self.double,
            "owner": self.owner_id,
        }


class Results(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True, index=True,
                unique=True, nullable=False)
    year = Column(Integer, unique=True)
    result = Column(JSON)
