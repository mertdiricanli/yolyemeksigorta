# Create your views here.
from web.models import *
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from web.forms import CreateUserForm, AuthForm

def index(request, user_form=None, auth_form=None):
	latestposts = Post.objects.all().order_by('-timestamp')[:5]
	if request.user.is_authenticated():
		# User logged in
		return render(request,'web/index.html',{'latests':latestposts,})
	else:
		# User not logged in
		user_form = user_form or CreateUserForm()
		auth_form = auth_form or AuthForm()
		return render(request,'web/index.html',{'latests':latestposts,'user_form':user_form,'auth_form':auth_form,})

def signup(request):
	user_form = CreateUserForm(data=request.POST)
	if request.method == 'POST':
		if user_form.is_valid():
			username = user_form.clean_username()
			password = user_form.clean_password2()
			user_form.save()
			user = authenticate(username=username, password=password)
			login(request,user)
			return redirect('/')
		else:
			return index(request, user_form=user_form)
	return redirect('/')

def login_view(request):
	if request.method == 'POST':
		form = AuthForm(data=request.POST)
		if form.is_valid():
			login(request,form.get_user())
			return redirect('/')
		else:
			return index(request, auth_form=form)
	return redirect('/')

def logout_view(request):
	logout(request)
	return redirect('/')
	
