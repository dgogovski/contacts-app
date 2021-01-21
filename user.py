from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
# from database import database

app = Flask(__name__)


class User:
	def __init__(self, user_id, name, number, hashed_pwd, timestamp):
		self.__id = user_id
		self.__name = name
		self.__number = number
		self.__hashed_pwd = hashed_pwd
		# self.timestamp_ = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		self.__timestamp = timestamp

	# def create(self):
	# 	values = (self.__name, self.__number, self.__hashed_pwd, self.__timestamp)
	# 	return database.create_user(values)

	@staticmethod
	def hash_password(password):
		return generate_password_hash(password)

	def verify_password(self, submit_password):
		return check_password_hash(self.__hashed_pwd, submit_password)

	# @staticmethod
	# def find_by_user_id(user_id):
	# 	if not user_id:
	# 		return None
	# 	with database() as db:
	# 		row = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
	# 		if row is not None:
	# 			return User(*row)
	#
	# @staticmethod
	# def find_by_username(username):
	# 	with database() as db:
	# 		row = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
	# 		if row is not None:
	# 			return User(*row)
	# 		app.logger.info('No user with this username exists.')
	# 		return None

	# @staticmethod
	# def find_by_number(number):
	# 	if not number:
	# 		return None
	# 	with DB() as db:
	# 		row = db.execute(
	# 			'SELECT * FROM users WHERE number = ?',
	# 			(number,)
	# 		).fetchone()
	# 		if row:
	# 			return User(*row)

	# Getters and setters
	def get_id(self):
		return self.__id

	def get_name(self):
		return self.__name

	def get_number(self):
		return self.__number

	def get_hashed_pwd(self):
		return self.__hashed_pwd

	def get_timestamp(self):
		return self.__timestamp
