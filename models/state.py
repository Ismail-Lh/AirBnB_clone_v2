#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_type
from models.city import City

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """

    if storage_type == "db":
        __tablename__ = "states"

        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all, delete")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes State"""
        super().__init__(*args, **kwargs)

    @property
    def cities(self):
        """returns the list of City instances"""
        from models import storage

        cities_instances = []
        all_cities = storage.all(City)

        for city in all_cities.values():
            if city.state_id == self.id:
                cities_instances.append(city)

        return cities_instances
