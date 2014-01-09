__author__ = 'justasic'

from django.shortcuts import render, render_to_response
from django.template.context import RequestContext

def index(request):
	ctx = RequestContext(request, {
			'posts': [],
		})

	return render_to_response('front/index.html', ctx)