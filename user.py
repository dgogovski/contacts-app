from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


class User:
	def __init__(self, user_id, name, number, hashed_pwd, timestamp):
		self.__id = user_id
		self.__name = name
		self.__number = number
		self.__hashed_pwd = hashed_pwd
		# self.timestamp_ = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		self.__timestamp = timestamp

	# Password hashing
	@staticmethod
	def hash_password(password):
		return generate_password_hash(password)

	def verify_password(self, submit_password):
		return check_password_hash(self.__hashed_pwd, submit_password)

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
