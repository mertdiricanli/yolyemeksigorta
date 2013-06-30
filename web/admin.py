# -*- coding:utf-8 -*-
from django.contrib import admin
from web.models import Sector, Company, Category, Post

admin.site.register(Sector)
admin.site.register(Company)
admin.site.register(Category)

class PostAdmin(admin.ModelAdmin):
	list_display = ('category', 'company', 'author')

admin.site.register(Post, PostAdmin)