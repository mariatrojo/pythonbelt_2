from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class BlogManager(models.Manager):
	def register_validator(self, postData):
		errors = []

		name = postData['name']
		alias = postData['alias']
		email = postData['email']
		pw = postData['password']
		conf_pw = postData['confirm_password']
		dob = postData['dob']

		if not name:
			errors.append("Name cannot be empty")
		elif len(name) < 2:
			errors.append("Name must be longer than 1 character")
		
		if not alias:
			errors.append("Alias cannot be empty")
		elif len(alias) < 2:
			errors.append("Alias must be longer than 1 character")
		elif not alias.isalpha():
			errors.append("Alias can only contain letters")

		if not email:
			errors.append("Email cannot be empty")
		elif not EMAIL_REGEX.match(email):
			errors.append("Invalid Email!")

		if not pw:
			errors.append("Password cannot be empty")
		elif len(pw) < 8:
			errors.append("Password must be 8 characters or longer")
		elif pw != conf_pw:
			errors.append("Passwords don't match")
		
		if not dob:
			errors.append("Date of birth cannot be empty")
		elif len(dob) < 8:
			errors.append("Date of birth must be 8 characters long")

		if not errors:
			try:
				User.objects.get(email=email)
				errors.append("Email is already used")
			except:
				hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
				return User.objects.create(name=name, alias=alias, email=email, dob=dob, password=hash)

		return errors

	def login_validator(self, postData):
		errors = []
		email = postData['email']
		pw = postData['password']

		if not email:
			errors.append("Email cannot be empty")
		elif not EMAIL_REGEX.match(email):
			errors.append("Invalid Email!")
		
		if not pw:
			errors.append("Password cannot be empty")
		elif len(pw) < 8:
			errors.append("Password must be 8 characters or longer")

		if not errors:
			try:
				user = User.objects.get(email=email)
				if bcrypt.checkpw(pw.encode(), user.password.encode()):
					return user
			except:
				errors.append("You aren't registered yet")

		return errors

class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	dob = models.DateField()
	friends = models.ManyToManyField("self")

	objects = BlogManager()

# SELECT users.first_name as user, users2.first_name as friend
# FROM users
# LEFT JOIN friendships
# ON users.id = friendships.user_id
# LEFT JOIN users as users2
# ON users2.id = friendships.friend_id