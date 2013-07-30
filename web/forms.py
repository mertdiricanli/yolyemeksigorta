# -*- coding:utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django import forms
from web.models import Sector, Company, Category, Post
from django.template.defaultfilters import slugify

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
			if f != '__all__':
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
			if f != '__all__':
				self.fields[f].widget.attrs.update({'placeholder': strip_tags(error)})
		return form

class CompanyForm(forms.ModelForm):
	sector = forms.ModelChoiceField(queryset=Sector.objects.all(),empty_label="Lütfen Seçiniz", label="Sektör")
	companyname = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder':'Şirket Adı'}), label="Şirket Adı")
	class Meta:
		model = Company
		exclude = ['companyslug']

	def is_valid(self):
		form = super(CompanyForm,self).is_valid()
		for f, error in self.errors.iteritems():
			if f != '__all__':
				self.fields[f].widget.attrs.update({'placeholder': strip_tags(error)})
		return form

class PostForm(forms.ModelForm):
	category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Kategori Seçiniz", label="Kategori")
	content =forms.CharField(widget=forms.widgets.Textarea(attrs={'rows':4}), label="Yorumunuz")
	class Meta:
		model = Post
		exclude = ['company','author', 'timestamp']

	def __init__(self, user, *args, **kwargs):
		self.user = user
		super(PostForm, self).__init__(*args, **kwargs)

	def is_valid(self):
		form = super(PostForm,self).is_valid()
		for f, error in self.errors.iteritems():
			if f != '__all__':
				self.fields[f].widget.attrs.update({'placeholder': strip_tags(error)})
		return form

