# -*- coding:utf-8 -*-
from web.models import *
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from web.forms import CreateUserForm, AuthForm, CompanyForm, PostForm
from django.db import IntegrityError
from django.http import Http404
from django.http import HttpResponse
import string

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
				return render(request, 'web/company.html', {'company':company, 'form': form},
					context_instance=RequestContext(request, processors=[authform]))
		else:
			form = PostForm(request.user)
		posts = Post.objects.filter(company=company.id).order_by('-timestamp')
		sectorCompanies = Company.objects.filter(sector=company.sector.id)[:4]
		return render(request, 'web/company.html', {'posts':posts, 'company':company, 'form': form, 'sectorCompanies':sectorCompanies},
			context_instance=RequestContext(request, processors=[authform]))
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
					return render(request, 'web/companies.html', {'companyform':form, 'errors': formerrors, 'companies':listcompanies},
						context_instance=RequestContext(request, processors=[authform]))
			else:
				form = CompanyForm()
			return render_to_response('web/companies.html',{'companyform':form, 'companies':listcompanies},
				context_instance=RequestContext(request, processors=[authform]))
		except IntegrityError:
			message = 'Bu şirket daha önce eklenmiş..'
			return render(request, 'web/companies.html',{'companyform':form, 'companies':listcompanies, 'message': message,})

def search(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		results = Company.objects.filter(companyname__icontains=q)
		return render(request, 'web/search.html', {'results':results, 'q':q,},
			context_instance=RequestContext(request, processors=[authform]))
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

		return render(request, 'web/sector.html', {'sectorCompanies':sectorCompanies, 'sector':sector},
			context_instance=RequestContext(request, processors=[authform]))
	else:
		letters = list(set([x for x in string.uppercase+string.digits]))
		letters.sort()
		if 'q' in request.GET and request.GET['q']:
			q = request.GET['q']
			sectorList = Sector.objects.filter(sectorname__istartswith=q)
			return render(request, 'web/sectors.html', {'letters': letters, 'sectorList': sectorList, 'q':q,},
				context_instance=RequestContext(request, processors=[authform]))
		else:
			return redirect('/sektorler/?q=A')	



