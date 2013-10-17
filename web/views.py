# -*- coding:utf-8 -*-
from django.conf import settings
from web.models import *
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from web.forms import CreateUserForm, AuthForm, CompanyForm, PostForm
from django.db import IntegrityError
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import string
# Google Plus OAuth
from django.contrib import messages
import datetime
import json
import urllib
import urlparse
from web import utils

def authform(request):
	return{
		'auth_form': AuthForm()
	}

def index(request, user_form=None, auth_form=None):
	latestposts = Post.objects.all().order_by('-timestamp')[:5]
	if request.user.is_authenticated():
		# User logged in
		return render(request,'web/index.html',{'latests':latestposts,})
	else:
		# User not logged in
		user_form = user_form or CreateUserForm()
		auth_form = auth_form or AuthForm()
		return render(request,'web/index.html',{'latests':latestposts,
			'user_form':user_form,'auth_form':auth_form,})


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

def google_login(request):
	""" Google+ OAuth2 login """
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')

	if 'error' in request.GET:
		messages.add_message(request, messages.ERROR,
			request.GET['error'])
		return HttpResponseRedirect('/')
	elif 'code' in request.GET:
		params = { \
			'client_id': settings.GOOGLEPLUS_CLIENT_ID, \
			'redirect_uri': settings.GOOGLE_REDIRECT_URI, \
			'client_secret': settings.GOOGLEPLUS_CLIENT_SECRET, \
			'code': request.GET['code'], \
			'grant_type': 'authorization_code', \
		}
		req = urllib.urlopen('https://accounts.google.com/o/oauth2/token',
			urllib.urlencode(params))
		if req.getcode() != 200:
			response = render_to_response('500.html', {}, \
					context_instance=RequestContext(request))
			response.status_code = 500
			return response

		response = req.read()
		response_query_dict = json.loads(response)
		access_token = response_query_dict['access_token']
		expires_in = response_query_dict['expires_in']
		profile = utils.api('people/me', {'access_token': access_token})
		getemailaddress = utils.get_email_address({'access_token': access_token})
		emailaddress = getemailaddress['email']
		googleplus_user = _create_or_update_googleplus_user(profile, emailaddress, access_token, expires_in)

		user = authenticate(googleplus_user=googleplus_user)
		if user is not None:
			if user.is_active:
				login(request, user)
				request.session.set_expiry(googleplus_user.expiry_at)
				if 'next' in request.GET:
					return HttpResponseRedirect(request.GET['next'])
				return HttpResponseRedirect('/')
			else:
				messages.add_message(request, messages.ERROR, "Account disabled.")
		else:
			messages.add_message(request, messages.ERROR, "Login failed.")
	else:
		params = { 
			'client_id': settings.GOOGLEPLUS_CLIENT_ID, 
			'redirect_uri': settings.GOOGLE_REDIRECT_URI, 
			'scope': 'https://www.googleapis.com/auth/plus.me', 
			'scope': 'https://www.googleapis.com/auth/userinfo.email', 
			'response_type': 'code', 
		}
		return HttpResponseRedirect('https://accounts.google.com/o/oauth2/auth?' +
			urllib.urlencode(params)
		)

def _create_or_update_googleplus_user(profile, emailaddress, access_token, expires_in):
	"""Creates or updates a Google+ user profile in local database.
	"""
	user_is_created = False
	try:
		googleplus_user = GooglePlusUser.objects.get(googleplus_id=profile['id'])
	except GooglePlusUser.DoesNotExist:
		first_name, last_name = _get_first_and_last_name(profile['displayName'])
		user = User.objects.create( \
			first_name=first_name,
			last_name=last_name,
			email=emailaddress,
			username='gplus_' + profile['id']
		)
		user_is_created = True

	if user_is_created:
		googleplus_user = GooglePlusUser()
		googleplus_user.googleplus_id = profile['id']
		googleplus_user.user = user
	else:
		first_name, last_name = _get_first_and_last_name(profile['displayName'])
		googleplus_user.user.first_name = first_name
		googleplus_user.last_name = last_name

	googleplus_user.googleplus_display_name = profile['displayName']
	googleplus_user.access_token = access_token
	googleplus_user.expiry_at = datetime.datetime.now() + \
		datetime.timedelta(seconds=int(expires_in))    
	googleplus_user.save()

	return googleplus_user

def _get_first_and_last_name(display_name):
	try:
		first_name, last_name = display_name.strip().rsplit(' ', 1)
	except ValueError:
		first_name = display_name
		last_name = ''
	return first_name, last_name

def companines(request, companyname=""):
	if companyname:
		try:
			company = Company.objects.get(companyslug=companyname)
		except Company.DoesNotExist:
			raise Http404
		if request.method == 'POST':
			form = PostForm(request.user, request.POST)
			if form.is_valid():
				myform = form.save(commit=False)
				myform.author = request.user
				myform.company = company
				myform.clean()
				myform.save()
				return redirect('/')
			else:
				return render(request, 'web/company.html', {'company':company, 'form': form})
		else:
			form = PostForm(request.user)
		posts = Post.objects.filter(company=company.id).order_by('-timestamp')
		sectorCompanies = Company.objects.filter(sector=company.sector.id).order_by('?').exclude(pk=company.id)[:3]
		return render(request, 'web/company.html', {'posts':posts, 'company':company, 'form': form, 'sectorCompanies':sectorCompanies})
	else:
		try:
			listcompanies = Company.objects.all().order_by('companyname')[:8]
			if request.method == 'POST':
				form = CompanyForm(request.POST)
				if form.is_valid():
					form.clean()
					form.save()
					return redirect('/')
				else:
					formerrors = form.errors
					return render(request, 'web/companies.html', {'companyform':form, 'errors': formerrors, 'companies':listcompanies})
			else:
				form = CompanyForm()
			return render(request, 'web/companies.html',{'companyform':form, 'companies':listcompanies})
		except IntegrityError:
			message = 'Bu şirket daha önce eklenmiş..'
			return render(request, 'web/companies.html',{'companyform':form, 'companies':listcompanies, 'message': message,})

def search(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		results = Company.objects.filter(companyname__icontains=q)
		return render(request, 'web/search.html', {'results':results, 'q':q,})
	else:
		message = 'Aramak için bir şeyler yazın'
		return HttpResponse(message)


def sectors(request, sectorname=""):
	if sectorname:
		try:
			sector = Sector.objects.get(sectorslug=sectorname)
			sectorCompanies = Company.objects.filter(sector=sector.id)
		except Sector.DoesNotExist:
			raise Http404

		return render(request, 'web/sector.html', {'sectorCompanies':sectorCompanies, 'sector':sector})
	else:
		letters = list(set([x for x in string.uppercase+string.digits]))
		letters.sort()
		if 'q' in request.GET and request.GET['q']:
			q = request.GET['q']
			sectorList = Sector.objects.filter(sectorname__istartswith=q)
			return render(request, 'web/sectors.html', {'letters': letters, 'sectorList': sectorList, 'q':q,})
		else:
			return redirect('/sektorler/?q=A')	

def users(request, username=""):
	if username:
		try:
			myuser = User.objects.get(username=username)
		except User.DoesNotExist:
			raise Http404
		userPosts = Post.objects.filter(author=myuser.id)
		return render(request, 'web/user.html', {'myuser':myuser, 'userPosts':userPosts})
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])







