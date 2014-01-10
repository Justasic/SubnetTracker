from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^cidradd/', 'SubnetTracker.apps.front.views.cidradd', name='cidradd'),
	url(r'^cidrremove/(\d+)/', 'SubnetTracker.apps.front.views.cidrremove', name='cidrremove'),
	url(r'^$', 'SubnetTracker.apps.front.views.index'),
)