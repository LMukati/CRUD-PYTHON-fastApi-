from tortoise.models import Model
from tortoise import Tortoise,fields
from enum import Enum

class Gender(str,Enum):
	MALE = 'Male'
	FEMALE = 'Female'
	OTHER = 'Other'

class Hobby(str,Enum):
	READING = 'Reading'
	GARDENING = 'Gardening'
	COOKING = 'Cooking'

class User(Model):
	name = fields.CharField(200)
	email = fields.CharField(200)
	mobile = fields.IntField()
	country = fields.CharField(200)
	state = fields.CharField(200)
	city = fields.CharField(200)
	image = fields.TextField()
	gender = fields.CharEnumField(enum_type=Gender)
	hobby = fields.CharEnumField(enum_type=Hobby)


class Persone(Model):
	email = fields.CharField(200)
	password = fields.CharField(200)

	

Tortoise.init_models(['user.models'],'models')	
	













