#!usr/bin/python3
"""
from Module : base.py
"""
from datetime import datetime
from uuid import uuid4
import models


class BaseModel():
    """
    a class BaseModel that defines all common
    attributes/methods for other classes
    """

    def __init__(self, *args, **kwargs):   
    """
    Instantation
    """
        if len(kwargs) > 0:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key == "created_at" or key == "updated_at":
                    value = datetime.fromisoformat(value)
                setattr(self, key, value)
            return

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        models.storage.new(self)
    
    def __str__(self):
        """
        should print: [<class name>] (<self.id>)
        <self.__dict__>
        """
        return "[{}]({})<{}>".format(type(self).__name__, self.id, self.__dict__)

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
        dict = self.__dict__
        dict['__class__'] = self.__class__.name
        dict['created_at'] = dict['created_at'].isoformat()
        dict['updated_at'] = dict['updated_at'].isoformat()

        return dict
