from django.db import models
from django.contrib.auth.models import User
import hashlib

class Sector(models.Model):
	sectorname = models.CharField(max_length=200)
	sectorslug = models.SlugField(max_length=200, unique=True)

class Company(models.Model):
	sector = models.ForeignKey('web.Sector')
	companyname = models.CharField(max_length=200)
	companyslug = models.SlugField(max_length=200, unique=True)

class Category(models.Model):
	categoryname = models.CharField(max_length=200)
	categoryslug  = models.SlugField(max_length=200, unique=True)

class Post(models.Model):
	category = models.ForeignKey('web.Category')
	company = models.ForeignKey('web.Company')
	author = models.ForeignKey(User)
	content = models.TextField()
	timestamp = models.DateField(auto_now_add=True)

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
	def gravatar_url(self):
		return "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(self.user.email).hexdigest()

