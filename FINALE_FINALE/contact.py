from datetime import datetime
from flask import Flask

app = Flask(__name__)


class Contact:
    def __init__(self, contact_id, name, number, note, user_id, activity=None):
        self.__id = contact_id
        self.__name = name
        self.__number = number
        self.__note = note
        self.__user_id = user_id
        self.__activity = activity

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_number(self):
        return self.__number

    def get_note(self):
        return self.__note

    def get_user_id(self):
        return self.__user_id

    def get_activity(self):
        return self.__activity

    def set_activity(self, activity):
        self.__activity = activity

    # # Database operations
    # def create(self):
    #     values = (self.__name, self.__number, self.__note, self.__user_id)
    #     return database.create_contact(values)
    #     # if database.create_contact(values) is True:
    #     #     return self
    #     # return False
    #
    # def update(self):
    #     values = (self.__name, self.__number, self.__note, self.__user_id)
    #     return database.update_contact(values)
    #
    # def delete(self):
    #     database.delete_contact(self.__contact_id)
    #
    # @staticmethod
    # def get_contacts():
    #     contacts = []
    #     rows = database.get_contacts()
    #     if rows is not False or None:
    #         for row in rows:
    #             contacts.append(Contact(*row))
    #         return contacts
    #     elif rows is False:
    #         app.logger.error('Could not get contacts.')
    #         return False
    #     app.logger.info('No contacts to get.')
    #     return None
    #
    # @staticmethod
    # def get_by_id(contact_id):
    #     row = database.get_contact_by_id(contact_id)
    #     if row is not False or None:
    #         return Contact(*row)
    #     elif row is False:
    #         app.logger.error('Could not get contact by id.')
    #         return False
    #     app.logger.info('No contact to get by id.')
    #     return None
    #
    # @staticmethod
    # def get_by_user_id(user_id):
    #     rows = database.get_contacts_by_user_id(user_id)
    #     if rows is not None and False:
    #         print(rows)
    #         contacts = []
    #         for row in rows:
    #             contact = Contact(*row)
    #             user_timestamp = database.get_user_timestamp(user_id)
    #             if user_timestamp is not None:
    #                 contact.active = True
    #                 timestamp = datetime.strptime(user_timestamp[0], '%Y-%m-%d %H:%M:%S')
    #                 seconds = (datetime.now() - timestamp).total_seconds()
    #                 contact.active = seconds < 10
    #                 contacts.append(contact)
    #             else:
    #                 return [Contact(*row) for row in rows]
    #         return contacts
    #     elif rows is False:
    #         app.logger.error('Could not get contact by user_id.')
    #         return False
    #     app.logger.info('No contact to get by user_id.')
    #     return None