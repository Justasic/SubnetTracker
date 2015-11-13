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
__author__ = 'justasic'

# Django imports
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseBadRequest
from ipaddress import IPv4Network, AddressValueError
import json

# Import our CIDR model
from SubnetTracker.apps.front.models import CIDR


class CIDRForm(ModelForm):
	""" This is an extension of the CIDR Model to make
		a nice Django Form out of it. This makes
		using the form and saving its data really
		easy.
	"""
	class Meta:
		model = CIDR


class AddressExists(Exception):
	""" This is really just to take advantage of the already
		needed try statement in the 'cidradd' function below.
		It makes it easy to return a response while including
		the CIDR object for reference.
	"""
	def __init__(self, message, cidr):
		Exception.__init__(self, message)
		self.cidr = cidr


def index(request):
	""" Renders and returns the index HTML page
		which lists all known CIDR masks and their names
		as well as a form to submit and check new CIDR masks
	"""
	ctx = RequestContext(request, {
			'cidrs': CIDR.objects.all(),
			'cidr_form': CIDRForm(),
		})

	return render_to_response('front/index.html', ctx)


def cidradd(request):
	""" Checks that the CIDR submitted is valid.
		If the CIDR is valid, it adds it to the database, updates the list, and updates
		any AJAX clients.

		If the CIDR is invalid, it returns and error and updates nothing.
	"""
	jsonresponse = {}
	# Make sure it's a post request or that the request is AJAX, otherwise give
	# a bad request error
	if request.is_ajax() or request.method == 'POST':
		form = CIDRForm(data=request.POST)
		if form.is_valid():
			# get the model without saving to the database.
			model = form.save(commit=False)
			try:
				# Check and make sure the CIDR mask is valid
				ip = IPv4Network(unicode(model.cidr))
				# Check that the CIDR mask doesn't already overlap an existing CIDR mask.
				for c in CIDR.objects.all():
					if c.CIDROverlaps(ip):
						raise AddressExists(u"CIDR address already exists", c)

				# Commit the form to the database.
				model = form.save()
				jsonresponse = {'success': model.id}
				del ip
			except (AddressValueError, ValueError):
				# Check that the CIDR mask is valid.
				jsonresponse = {'error': 'Invalid CIDR mask'}
			except AddressExists as e:
				# Check that the CIDR mask doesn't exist already.
				jsonresponse = {'error': e.message, 'id': e.cidr.id, 'name': e.cidr.name}
			except:
				# Some other error that requires debugging. Return a generic error.
				jsonresponse = {'error': 'Server error'}
				raise
		else:
			jsonresponse = {'error': 'Please fill out all form fields'}
	else:
		# this really should return a 400 error.
		jsonresponse = {'error': 'Request must be ajax or POST'}

	# Return our response.
	return HttpResponse(json.dumps(jsonresponse), content_type='application/json')


def cidrremove(request, row_id):
	""" This function is the AJAX function which
		removes a CIDR address from the database
		as long as it exists.

		If the requested data does not exist, send a bad request.
	"""
	obj = CIDR.objects.filter(id=row_id)
	if obj:
		obj.delete()
	else:
		return HttpResponseBadRequest

	return HttpResponse(json.dumps({'success': u"Successfully deleted item %s" % row_id}), \
						content_type='application/json')


def cidrlist(request):
	""" This function returns a JSON encoded list of all the
		CIDR addresses, names, and database ids.
		This will be called every 2 or 5 seconds as an AJAX
		call to check for any change in the list of known
		CIDR addresses.
	"""
	cidrobjects = []

	for c in CIDR.objects.all():
		cidrobjects.append({'name': c.name, 'mask': c.cidr, 'id': c.id})
	return HttpResponse(json.dumps(cidrobjects), content_type='application/json')
