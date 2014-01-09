__author__ = 'justasic'

# Django imports
from django.shortcuts import render, render_to_response
from django.template.context import RequestContext
from django.forms import ModelForm
from django.http import HttpResponse
import json

# Our imports
from SubnetTracker.apps.front.models import CIDR

class CIDRForm(ModelForm):
	class Meta:
		model = CIDR

def index(request):
	ctx = RequestContext(request, {
			'cidr': CIDR.objects.all(),
			'cidr_form': CIDRForm(),
		})

	return render_to_response('front/index.html', ctx)


def cidrcheck(request):

	pass

def cidrremove(request):
	pass