from django.conf.urls import patterns,url
from rest_framework.urlpatterns import format_suffix_patterns
from alertcollector import views

urlpatterns = patterns('alertcollector.views',
    url(r'^generators/add/$',views.add_generator,name='add_generator'),
    url(r'^generators/del/',views.delete_generator,name='delete_generator'),
    url(r'^generators/update/',views.update_generator,name='update_generator'),	
    url(r'^generators/verify/',views.verify_generator,name='verify_generator'),
    url(r'^groups/add/',views.add_group,name="add_group"),
    url(r'^groups/verify/',views.verify_group,name="verify_group"),
    url(r'^groups/update/',views.update_group,name="update_group"),
    url(r'^groups/del/',views.delete_group,name="delete_group"),
    url(r'^class/add/',views.add_class,name="add_class"),
)
urlpatterns = format_suffix_patterns(urlpatterns)

