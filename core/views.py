from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render_to_response, render
from core.models import Hit, UserUrl, UserKey
import redis
from celery import task
from sitegate.decorators import sitegate_view

@task
def hit(seq):
	us = UserUrl.objects.filter(sequence = seq)
	for u in us:
		h = Hit.objects.create(url =u)


def add(request):
	api_key = request.REQUEST.get('api_v1', None)
	try:
		if api_key is None:
			raise Exception()
		user = UserKey.objects.get(key = api_key).user
		seq = request.REQUEST.get('seq', None)
		url = request.REQUEST.get('url')

		UserUrl.objects.create(user = user, sequence = seq, url = url)
		return HttpResponse()
	except:
		return HttpResponseForbidden()


def get(request, sequence):
	r = redis.Redis()
	a = r.get(sequence)
	if a is None:
		return HttpResponseRedirect('/')
	hit.delay(sequence)
	return HttpResponseRedirect(a)


def index(request):
	return render_to_response('index.html')

@sitegate_view
def entrance(request):
	return render(request, 'register.html', {'title':'Sign In & Sign Up'})


