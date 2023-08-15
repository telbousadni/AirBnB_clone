#!/usr/bin/python3
"""
the hbnb console version 1.0
entry point of the command line interpreter
"""

import cmd
import sys
from models import storage
from models.user import User
from models.state import State
from models.review import Review
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class HBNBCommand(cmd.Cmd):
    """console class:
        entry point of the command interpreter of our Hbnb Console
    """

    prompt = "(hbnb) "

    def do_EOF(self, line):
        """EOF command to exit the program with ctrl+D"""
        print()
        """delete print() if checker misbehaves"""
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """an empty line + ENTER shouldn’t execute anything"""
        pass

    def remove_quotations(self, args):
        """removes the quotations and commas from the arguments"""

        for i in range(len(args)):
            if args[i][0] in ('"', "'"):
                args[i] = args[i].replace('"', "").replace("'", "")
        return args

    def do_create(self, line):
        """Create command: creates a new instance of BaseModel
        saves it and prints its id
        Ex: $ create BaseModel
        """

        if (self.errors(line, "create") == 1):
            return False
        """ evaluate the contents of line string to class and execute it
        with ()"""
        instance = eval(line)()
        """save it to JSON file"""
        instance.save()
        print(instance.id)

    def do_show(self, line):
        """Show command: prints a string rep of an instance
        based on the class name and id
        Ex: $ show BaseModel 1234-1234-1234
        """

        if (self.errors(line, "show") == 1):
            return False
        """split line to multiple args"""
        args = line.split()
        """get all instances's dicts from storage"""
        instances_dict = storage.all()
        """remove the quotations if string inputted has them"""
        args = self.remove_quotations(args)
        print(instances_dict[args[0] + '.' + args[1]])

    def counter(self, cls_name):
        """this methods prints the num of instances of each class"""

        num_of_instances = 0
        instances_dict = storage.all()
        for inst in instances_dict.values():
            if inst.__class__.__name__ == cls_name:
                num_of_instances += 1
        print(num_of_instances)

    def do_destroy(self, line):
        """Destroy command: deletes an instance based on the class name and id
        Ex: $ destroy BaseModel 1234-1234-1234
        """
        if (self.errors(line, "destroy") == 1):
            return False

        instances_dict = storage.all()
        args = line.split()
        args = self.remove_quotations(args)
        del instances_dict[args[0] + '.' + args[1]]
        storage.save()

    def do_update(self, line):
        """Updates an instance based on the class name and id
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        if (self.errors(line, "update") == 1):
            return False

        args = line.split()
        instances_dict = storage.all()
        args = self.remove_quotations(args)
        x = args[0] + '.' + args[1]
        new_key = args[2]
        """ typecast only if it's a number so it can appear without quotes
        in the dict """
        if args[3].isdigit():
            new_value = eval(args[3])
        else:
            new_value = args[3]
        setattr(instances_dict[x], new_key, new_value)
        storage.save()

    def do_all(self, line):
        """all command: prints all string representation of all
        instances based or not on the class name.
        Ex: $ all BaseModel or $ all
        """
        instances_dict = storage.all()
        """if all is used without class name"""
        d_list = []
        if line == "":
            d_list = [str(i) for i in instances_dict.values()]
            print(d_list)
            return False
        args = line.split()
        """if all is used with class name, manage errors, if any, and return"""
        if (self.errors(line, "all") == 1):
            return False
        for i in instances_dict.values():
            if i.__class__.__name__ == args[0]:
                d_list.append(str(i))
        print(d_list)

    def errors(self, line, cmd):
        """manages error messages for user input"""

        cls_list = [
                "BaseModel", "User", "State", "City",
                "Amenity", "Place", "Review"
                ]
        cmd_list = ["create", "show", "all", "destroy", "update"]

        if line == "":
            print("** class name missing **")
            return 1
        args = line.split()
        if args[0] not in cls_list and cmd in cmd_list:
            print("** class doesn't exist **")
            return 1
        elif cmd in ["create", "all"]:
            return 0

        if len(args) < 2 and cmd in ["show", "destroy", "update"]:
            print("** instance id missing **")
            return 1

        instances_dict = storage.all()
        args = self.remove_quotations(args)
        k = args[0] + '.' + args[1]

        if k not in instances_dict and cmd in ["show", "destroy", "update"]:
            print("** no instance found **")
            return 1
        elif cmd in ["show", "destroy"]:
            return 0

        if len(args) < 3 and cmd == "update":
            print("** attribute name missing **")
            return 1
        if len(args) < 4 and cmd == "update":
            print("** value missing **")
            return 1
        return 0

    def default(self, line):
        """ this is the default function"""

        cls_list = [
                    "BaseModel", "User", "State", "City",
                    "Amenity", "Place", "Review"
                ]
        console_commands = {
                "show": self.do_show, "all": self.do_all,
                "destroy": self.do_destroy, "update": self.do_update,
                "create": self.do_create, "count": self.counter
                }

        """ replace those delimeters with spaces"""
        new_line = line.maketrans(";.(),{}:", "        ")
        line = line.translate(new_line)
        """ seperate into args except if command doesn't exist"""
        try:
            cls, cmd, *args = line.split()
        except Exception as e:
            print("** Unknown syntax", file=sys.stderr)
            return False

        """ loop over dictionnary of cmds and execute the appropriate method"""
        if cls in cls_list:
            for k, v in console_commands.items():
                if cmd == k:
                    """ count is seperate cause it takes only one arg:
                    cls_name"""
                    if cmd == "count":
                        v(cls)
                    elif cmd == "update":
                        """ update works with dict or without
                        dict is translated into normal args so it's a list
                        we loop over args, 2 at a time, to take key and value
                        we call the method v with 1 pair at a time untill
                        args is over"""
                        for i in range(1, len(args), 2):
                            x = cls + ' ' + args[0] + ' ' +\
                                args[i] + ' ' + args[i + 1]
                            v(x)
                    else:
                        v(cls + ' ' + (" ".join(args)))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
