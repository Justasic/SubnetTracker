__author__ = 'justasic'

# Django imports
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseBadRequest
from ipaddress import IPv4Network, AddressValueError
import json

# Our imports
from SubnetTracker.apps.front.models import CIDR


class CIDRForm(ModelForm):
	""" This is an extension of the CIDR Model to make
		a nice Django Form out of it. This makes using
		the Model easier with the Form.
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
	if request.is_ajax() or request.method == 'POST':
		form = CIDRForm(data=request.POST)
		if form.is_valid():
			# get the model without saving to the database.
			model = form.save(commit=False)
			try:
				ip = IPv4Network(unicode(model.cidr))

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
				jsonresponse = {'error': 'Server error'}
				raise
		else:
			jsonresponse = {'error': 'Request must be ajax or POST'}
	else:
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