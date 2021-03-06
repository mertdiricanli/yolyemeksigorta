# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import hashlib
from django.template.defaultfilters import slugify
from yolyemeksigorta.utils import downcode

class Sector(models.Model):
	sectorname = models.CharField(max_length=200)
	sectorslug = models.SlugField(max_length=200, unique=True)
	def __unicode__(self):
		return '%s'  % self.sectorname

class Company(models.Model):
	sector = models.ForeignKey('web.Sector')
	companyname = models.CharField(max_length=200)
	companyslug = models.SlugField(max_length=200, unique=True)
	def __unicode__(self):
		return '%s' % self.companyname

	def save(self, *args, **kwargs):
		self.companyslug = slugify(downcode(self.companyname)) 
		super(Company,self).save(*args, **kwargs)

class Category(models.Model):
	categoryname = models.CharField(max_length=200)
	categoryslug  = models.SlugField(max_length=200, unique=True)
	def __unicode__(self):
		return '%s' % self.categoryname

class Post(models.Model):
	category = models.ForeignKey('web.Category')
	company = models.ForeignKey('web.Company')
	author = models.ForeignKey(User)
	content = models.TextField()
	timestamp = models.DateField(auto_now_add=True)
	def gravatar_url(self):
		return "http://www.gravatar.com/avatar/%s?s=50&d=mm" % hashlib.md5(self.author.email).hexdigest()

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
	def gravatar_url(self):
		return "http://www.gravatar.com/avatar/%s?s=50&d=mm" % hashlib.md5(self.user.email).hexdigest()

class GooglePlusUser(models.Model):
	"""Stores Google+ user specific details. 
	"""
	user = models.OneToOneField(User)
	access_token = models.TextField()
	expiry_at = models.DateTimeField(null=True)
	googleplus_id = models.CharField(max_length=100, unique=True, db_index=True)
	googleplus_display_name = models.CharField(max_length=100, unique=True, db_index=True)

	def __unicode__(self):
		return unicode(self.id) + u' | ' + unicode(self.googleplus_id)

