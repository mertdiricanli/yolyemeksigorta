# Create your views here.
from web.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
	latestposts = Post.objects.all().order_by('-timestamp')[:5]
	return render_to_response('web/index.html',{'latests':latestposts}, context_instance=RequestContext(request))
	