from typeclasses.objects import Object
from random import randint
from evennia import Command as BaseCommand

class Phone(Object):
    def at_object_creation(self):
        self.db.number = Phone.find_new_number()
        self.db.texts = []
        self.db.notification_text = "Your phone beeps."

    def find_new_number(self):
        new_number = 0
        while new_number == 0:
            loop = 0
            all_phones = Phone.objects.all()
            max_loop = len(all_phones)
            for obj in all_phones:
                if obj.db.number == pot_num:
                    pot_num = randint(1000000, 9999999)
                    break
                if loop == max_loop:
                    new_number = pot_num
        return new_number

    def text(self, recipient, message):
        recipient.db.texts.append(self.db.number + "#;" + message)
        recipient.location.msg_contents(recipient.db.notification_text)


class CmdAbilities(Command):
    """
    List abilities

    Usage:
      abilities

    Displays a list of your current ability values.
    """
    key = "text"
    aliases = ["txt"]
    lock = 'cmd:holds("Phone")'
    help_category = "Phone"

    def func(self):
        "implements the actual functionality"

        caller = self.caller
        error_msg = "Usage: text <number> <message>"

        args = self.args
        if not args:
            for message in self.db.texts:
                caller.msg(message)
            return

        args_list = args.split()

        target_phone = self.search(args_list[0])
        text_message = args_list[1]

        if target_phone:
            if text_message:
                target_phone.db.texts.append(text_message)
            else:
                caller.msg(error_msg)
                return
        else:
            caller.msg(error_msg)
            return
