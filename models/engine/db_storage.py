#!/usr/bin/python3

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """This class manages storage of hbnb models in a database"""

    __engine = None
    __session = None

    def __init__(self):
        """Initializes database storage"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db_name = getenv("HBNB_MYSQL_DB")
        db_env = getenv("HBNB_ENV")

        db_url = "mysql+mysqldb://{}:{}@{}/{}".format(user, pwd, host, db_name)

        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if db_env == "test":
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """Reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
            )

        self.__session = Session()

    def all(self, cls=None):
        """Query on the current database session (self.__session)
        all objects depending of the class name (argument cls)"""
        all_classes = [User, Place, State, City, Amenity, Review]
        result = {}

        if cls is not None:
            if id is not None:
                obj = self.__session.query(cls).get(id)

                if obj is not None:
                    cls_name = obj.__class__.__name__
                    obj_key = cls_name + "." + str(obj.id)
                    result[obj_key] = obj
            else:
                for obj in self.__session.query(cls).all():
                    cls_name = obj.__class__.__name__
                    obj_key = cls_name + "." + str(obj.id)
                    result[obj_key] = obj
        else:
            for cla in all_classes:
                if id is not None:
                    obj = self.__session.query(cla).get(id)

                    if obj is not None:
                        cls_name = obj.__class__.__name__
                        obj_key = cls_name + "." + str(obj.id)
                        result[obj_key] = obj
                else:
                    for obj in self.__session.query(cla).all():
                        cls_name = obj.__class__.__name__
                        obj_key = cls_name + "." + str(obj.id)
                        result[obj_key] = obj
        return result

    def new(self, obj):
        """Add the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)
