"""
    Copyright (C) 2014-2015  Justin Crawford <Justasic@gmail.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^cidradd/', 'SubnetTracker.apps.front.views.cidradd', name='cidradd'),
	url(r'^cidrremove/(\d+)/', 'SubnetTracker.apps.front.views.cidrremove', name='cidrremove'),
	url(r'^cidrlist/', 'SubnetTracker.apps.front.views.cidrlist', name='cidrlist'),
	url(r'^$', 'SubnetTracker.apps.front.views.index'),
)
