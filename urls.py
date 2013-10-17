from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
import settings
admin.autodiscover()
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# 

urlpatterns = patterns('',
	url(r'^$', 'web.views.index'),
	url(r'^signup/$', 'web.views.signup'),
	url(r'^login/$', 'web.views.login_view'),
	url(r'^logout/$', 'web.views.logout_view'),
	url(r'^sirketler/$', 'web.views.companines'),
	url(r'^sirketler/(?P<companyname>[-\w]+)/$', 'web.views.companines'),
	url(r'^sektorler/$', 'web.views.sectors'),
	url(r'^sektorler/(?P<sectorname>[-\w]+)$', 'web.views.sectors'),
	url(r'^search/$', 'web.views.search'),
	url(r'^(?P<username>[-\w]+)/$', 'web.views.users'),
	url(r'^googleplus/login/$', 'web.views.google_login', name="googleplus_login"),
	# Examples:
	# url(r'^$', 'yolyemeksigorta.views.home', name='home'),
	# url(r'^yolyemeksigorta/', include('yolyemeksigorta.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^a/admin/', include(admin.site.urls)),
	url(r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),

	# Django Password Reset
	url(r'^user/password/reset/$', 'django.contrib.auth.views.password_reset',
		{'post_reset_redirect' : '/user/password/reset/done'}, name='password_reset'),
	url(r'^user/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
	url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
		'django.contrib.auth.views.password_reset_confirm',
		{'post_reset_redirect' : '/user/password/done/'}),
	url(r'^user/password/done/$', 'django.contrib.auth.views.password_reset_complete'),

)
