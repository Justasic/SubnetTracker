from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^cidrcheck/', 'SubnetTracker.apps.front.views.cidrcheck', name='cidrcheck'),
	url(r'^$', 'SubnetTracker.apps.front.views.index'),
)