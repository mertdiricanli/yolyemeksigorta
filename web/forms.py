# -*- coding:utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django import forms

class CreateUserForm(UserCreationForm):
	email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':'Email','class':'input-large'}))
	username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':'Kullanıcı Adı','class':'input-large'}))
	first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':'Ad','class':'input-large'}))
	last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder':'Soyad','class':'input-large'}))
	password1 = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder':'Şifre','class':'input-large'}))
	password2 = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder':'Şifre Tekrar','class':'input-large'}))

	def is_valid(self):
		form = super(CreateUserForm,self).is_valid()
		for f, error in self.errors.iteritems():
			if f != '__all_':
				self.fields[f].widget.attrs.update({'class':'error', 'value': strip_tags(error)})
		return form

	class Meta:
		fields = ['first_name','last_name','username','email','password1','password2']
		model = User

class AuthForm(AuthenticationForm):
	username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder':'Kullanıcı Adı','class':'input-small'}))
	password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder':'Şifre','class':'input-small'}))

	def is_valid(self):
		form = super(AuthForm,self).is_valid()
		for f, error in self.errors.iteritems():
			if f != '__all_':
				self.fields[f].widget.attrs.update({'value': strip_tags(error)})
		return form