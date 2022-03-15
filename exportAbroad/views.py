# views from the main site
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from newmarkets.views import feasability	

from .forms import ProfileForm, CompanyForm
from company.models import Company
from django.http import JsonResponse, HttpResponse

def promo(request):
    return render(request, 'promo.html')

def topcountries(request):
    return render(request, 'topcountries.html')

def topcountries2(request):
    return render(request, 'topcountries2.html')

def settings(request):
	# needed to get the user profile saved, by user logged in
	user_name = None
	if request.user.is_authenticated():
		user_name = request.user.username
	
	#print "AAAAA" + request.user.username
	
	try:	
		current_user = User.objects.get(username=user_name)
		print current_user.id
	except User.DoesNotExist:
		current_user = None
		print 'User not found'
	
	try:
		test = Company.objects.filter(user=request.user.id)
	except Company.DoesNotExist:
		test = None
		print 'In Company the current user does not exist'	
	
	context = dict()
	context['current_user'] = request.user.id
	context['company'] = test
	
	"""
	#print "company: " + str(test)
	#print "user: " + str(current_user)

	form = ProfileForm()
	if request.method == "POST":
		print request.POST['first_name']
		print request.POST['last_name']
		print request.POST['phone']
		print request.POST['timezone']
		print request.POST['language']
		form = ProfileForm(request.POST, request.FILES)
		print request.FILES['docfile']
		if form.is_valid():
			#form = ProfileForm(profile_img = request.FILES['docfile'])
			my_model = form.save(commit=False) #without commit=False it gives error that the table doesn't exist http://prntscr.com/a69jfz
		else:
			form = ProfileForm()
			
	else:
		print "no se ha recibido nada"
	
	context = {
        'form': form
    }
	
	return render(request, 'account/settings_overview.html', context) , {'current_user', current_user}
	"""
	
	return render(request, 'account/settings_overview.html', context)

def settings_profile(request):
	form = ProfileForm()
	test = request.POST.get("first_name","")
	print request.POST.get('first_name',"")
	print request.POST.get('last_name',"")
	print request.POST.get('phone',"")
	print request.POST.get('timezone',"")
	print request.POST.get('language',"")
	print request.FILES.get('docfile', "")
	form = ProfileForm(request.POST, request.FILES)
	if form.is_valid():
		my_model = form.save() #commit=False
	else:
		form = ProfileForm()
	try:
		response_data = JsonResponse({'result': 'Saved successfully.', 'message': test})
	except:
		response_data = JsonResponse({'result': 'Error', 'message': 'The process did not run correctly.'})

	return HttpResponse(response_data, content_type="application/json")
	
def settings_company(request):
	form = CompanyForm()
	test = request.POST.get("company_name","")
	print request.POST.get("company_name","")
	response_data = JsonResponse({'result': 'Saved successfully.', 'message': test})
	form = CompanyForm(request.POST)
	if form.is_valid():
		my_model = form.save() #commit=False
	else:
		form = CompanyForm()
	try:
		response_data = JsonResponse({'result': 'Saved successfully.', 'message': test})
	except:
		response_data = JsonResponse({'result': 'Error', 'message': 'The process did not run correctly.'})

	return HttpResponse(response_data, content_type="application/json")
	
def users_permission(request):
	# needed to get all company users filtered by company. company will be got from 'company_name' field of settings_overview.html
	response_data = JsonResponse({'result': 'Saved successfully.', 'message': test})
	return HttpResponse(response_data, content_type="application/json")
	
def blog(request):
    return redirect('http://blog.exportabroad.com/')

@login_required
def dashboard(request):
    #return render(request, 'dashboard.html')
    return render(request, 'app/dashboard.html')


@login_required
def customerlist(request):
    return render(request, 'app/customers/customerlist.html')

@login_required
def customer(request):
    return render(request, 'app/customers/customer.html')
