#!usr/bin/python3
"""
from Module : base.py
"""
from datetime import datetime
from uuid import uuid4
import models


class Basemodel():
    """
    a class BaseModel that defines all common
    attributes/methods for other classes
    """

    def __init__(self):   
    """
    Instantation
    """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def __str__(self):
        """
        should print: [<class name>] (<self.id>)
        <self.__dict__>
        """
        return "[{}]({})<{}>".format(self.__name__, self.id, self.__dict__)

    def save(self):
        """
        updates the public instance attribute
        updated_at with the current datetime
        """
        self.updated_at = datetime.now()

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
