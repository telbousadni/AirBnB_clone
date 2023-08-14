#!usr/bin/python3
"""
from Module : base.py
"""
from datetime import datetime
from uuid import uuid4
import models


class BaseModel:
    """defines all common attributes/methods for other classes """
    def __init__(self):
        """
        Instantation
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        models.storage.new(self)

    def __str__(self):
        """
        should print: [<class name>] (<self.id>)
        <self.__dict__>
        """
        return "[{}]({})<{}>".format(
                type(self).__name__, self.id, self.__dict__)

    def save(self):
        """
        updates the public instance attribute
        updated_at with the current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all
        keys/values of __dict__ of the instance
        """
        adict = (dict)self.__dict__
        adict["__class__"] = self.__class__.name
        adict["created_at"] = adict['created_at'].isoformat()
        adict["updated_at"] = adict['updated_at'].isoformat()

        return adict
