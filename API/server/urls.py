from django.conf.urls import patterns,url
from rest_framework.urlpatterns import format_suffix_patterns
from server import views

urlpatterns = patterns('server.views',
	url(r'^instance/',views.instance_create,name="instance"),
	url(r'^profile/',views.profile_alert,name="profile"),
	)

urlpatterns = format_suffix_patterns(urlpatterns)

