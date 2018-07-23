from django.shortcuts import render,render_to_response
from django.http.response import HttpResponse
from phoneNum.forms import dclxxbform
from django.forms import formset_factory
from .models import dclxxb
from django.contrib.auth.decorators import login_required
from django.template import *  
@login_required
def test(request):
	df = formset_factory(dclxxbform)
	username=request.user.username
	if request.method =='POST':
		postdata = df(request.POST)
		# print (postdata)
		if postdata.is_valid():
			for p in postdata:
				p.save()
		else:
			print ('bad')
		return HttpResponse('testpostdata')
	# form = dwxxform()
	else:

		dcl = dclxxb.objects.all()
		dclxxbformset = formset_factory(dclxxbform,extra=2,can_order=True,can_delete=True)
		dclxxbformset = dclxxbformset()
		for x in dcl:
			print (x.ybh)
		return render_to_response('test.html',{'f':dclxxbformset,'dcl':dcl,'username':username})
