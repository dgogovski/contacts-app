from flask import Flask
from datetime import datetime
from contact import Contact
from user import User
import sqlite3

app = Flask(__name__)
DB_NAME = 'database.db'
conn = sqlite3.connect(DB_NAME)


conn.cursor().execute('''
    CREATE TABLE IF NOT EXISTS contacts
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        number TEXT UNIQUE NOT NULL,
        note TEXT NOT NULL,
        user_id INTEGER
    )		
''')

conn.cursor().execute('''
    CREATE TABLE IF NOT EXISTS users
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        number TEXT UNIQUE NOT NULL,
        hashed_pwd TEXT NOT NULL,
        timestamp_ TEXT NOT NULL
    )		
''')


conn.commit()


class database:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, db_type, value, traceback):
        self.conn.commit()

    # User methods
    @staticmethod
    def create_user(user):
        with database() as db:
            # try:
            values = (user.get_name(), user.get_number(), user.get_hashed_pwd(), user.get_timestamp())
            db.execute('INSERT INTO users (name, number, hashed_pwd, timestamp_) VALUES (?, ?, ?, ?)', values)
            # 	return True
            # except:
            # 	app.logger.error('Could not create user.')
            # 	return False

    @staticmethod
    def get_user_by_id(user_id):
        with database() as db:
            print('get_user_by_id:user_id:', user_id)
            row = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            if row is None or False:
                app.logger.info('No users to get by this name')
                return None
            return User(*row)

    @staticmethod
    def get_user_by_name(name):
        with database() as db:
            row = db.execute('SELECT * FROM users WHERE name = ?', (name,)).fetchone()
            if row is None:
                app.logger.info('No users to get by this name')
                return None
            return User(*row)

    @staticmethod
    def get_user_timestamp(user):
        # TODO database without ()?
        with database() as db:
            return db.execute('SELECT timestamp_ FROM users WHERE id = ?', (user.get_id(),)).fetchone()

    # Contact methods
    @staticmethod
    def create_contact(contact):
        with database() as db:
            # try:
            values = (contact.get_name(), contact.get_number(), contact.get_note(), contact.get_user_id())
            db.execute('INSERT INTO contacts (name, number, note, user_id) VALUES (?, ?, ?, ?)', values)
            return True
        # except:
        # 	app.logger.error('Could not create contact.')
        # 	return False

    @staticmethod
    def update_contact(contact):
        with database() as db:
            # try:
            values = (contact.get_name(), contact.get_number(), contact.get_note(), contact.get_id())
            db.execute('UPDATE contacts SET name = ?, number = ?, note = ? WHERE id = ?', values)
            return True
        # except:
        # 	app.logger.error('Could not update contact.')
        # 	return False

    @staticmethod
    def delete_contact(contact):
        with database() as db:
            # try:
            db.execute('DELETE FROM contacts WHERE id = ?', (contact.get_id(),))
            return True
        # except:
        # 	app.logger.error('Could not update contact.')
        # 	return False

    @staticmethod
    def get_contacts():
        with database() as db:
            return db.execute('SELECT * FROM contacts')

    @staticmethod
    def get_contact_by_id(contact_id):
        with database() as db:
            # try:
            row = db.execute('SELECT * FROM contacts WHERE id = ?', (contact_id,)).fetchone()
            if row is None or False:
                return None
            return Contact(*row)
        # except:
        # 	app.logger.error('Could not get contact by id.')
        # 	return False

    # @staticmethod
    # def get_contacts_by_user_id(user):
    # 	with database() as db:
    # 		# try:
    # 		rows = db.execute('SELECT * FROM contacts WHERE user_id = ?', (user.get_id(),)).fetchall()
    # 		contacts = []
    # 		if rows is not False:
    # 			for row in rows:
    # 				contacts.append(Contact(*row))
    # 			return contacts
    # 		return None
    # 		# except:
    # 		# 	app.logger.error('Could not get contacts by user_id.')
    # 		# 	return False

    @staticmethod
    def get_contacts_by_user_id(user):
        if user is not None:
            user_id = user.get_id()
            with database() as db:
                # try:
                rows = db.execute('SELECT * FROM contacts WHERE user_id = ?', (user_id,)).fetchall()
                contacts = []
                if rows is not False:
                    for row in rows:
                        contact = Contact(*row)
                        user_contact = database.get_user_by_name(contact.get_name())
                        user_timestamp = database.get_user_timestamp(user_contact)
                        # user_timestamp = db.execute('SELECT timestamp_ FROM users WHERE number = ?',
                        #                             (contact.number,)).fetchone()
                        print('user_timestamp[0]:', user_timestamp[0])
                        if user_timestamp is not None:
                            # TODO store True as a string instead?
                            contact.set_activity(True)
                            timestamp = datetime.strptime(user_timestamp[0], '%Y-%m-%d %H:%M:%S')
                            seconds = (datetime.now() - timestamp).total_seconds()
                            print('seconds:', seconds)
                            # contact.set_activity(seconds < 10)
                            if seconds < 10:
                                contact.set_activity('Online')
                            else:
                                contact.set_activity('Offline')
                            contacts.append(contact)
                        else:
                            # No timestamp
                            return [Contact(*row) for row in rows]
                    return contacts
                else:
                    app.logger.info('No contacts with this user id.')
                    return None
        # User does not exist
        app.logger.error('User does not exist.')
        return False
        # except:
        # 	app.logger.error('Could not get contacts by user_id.')
        # 	return False

    # Ping method
    @staticmethod
    def ping(user):
        with database() as db:
            try:
                print('user:', user)
                values = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user.get_id())
                print('0:', values[0])
                print('1:', values[1])
                db.execute('UPDATE users SET timestamp_ = ? WHERE id = ?', values)
            except:
                app.logger.error('Error pinging.')
