#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        mos_ocname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(mos_ocname, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        mos_odict = FileStorage.__objects
        mos_objdict = {
                obj: mos_odict[obj].to_dict() for obj in mos_odict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(mos_objdict, f, indent=4)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path) as f:
                mos_objdict = json.load(f)
                for o in mos_objdict.values():
                    mos_cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(mos_cls_name)(**o))
        except FileNotFoundError:
            return
