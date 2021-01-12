from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from users.models import *
from .forms import UserLogin,SignUpForm
from django.core.mail import send_mail
from django.conf import settings


def changepassword(request):
	if not request.user.is_authenticated:
		return redirect('/')
	'''
	Please work on me -> success & error messages & style templates
	'''
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save(commit=True)
			update_session_auth_hash(request,user)

			messages.success(request,'Password changed successfully',extra_tags = 'alert alert-success alert-dismissible show' )
			return redirect('accounts:changepassword')
		else:
			messages.error(request,'Error,changing password',extra_tags = 'alert alert-warning alert-dismissible show' )
			return redirect('accounts:changepassword')
			
	form = PasswordChangeForm(request.user)
	return render(request,'accounts/change_password_form.html',{'form':form})




# from .forms import SignUpForm
from django.shortcuts import render, redirect

def signup_view(request):
	form = SignUpForm(request.POST)
	if form.is_valid():
		user = form.save()
		user.refresh_from_db()
		user.employee.first_name = form.cleaned_data.get('first_name')
		user.employee.last_name = form.cleaned_data.get('last_name')
		user.employee.email = form.cleaned_data.get('email')
		membership = Membership.objects.filter(name='Free').first()
		print(membership)
		user.employee.membership = membership
		user.employee.save()
		user.save()
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password1')
		user = authenticate(username=username, password=password)
		login(request, user)
		return redirect('accounts:login')
	else:
		if request.POST:
			form = SignUpForm()
			messages.error(request, "Follow Password Rules", extra_tags='alert alert-warning alert-dismissible show')
	return render(request, 'accounts/register.html', {'form': form,'profile': True})


def signup_view1(request):
	if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
		messages.error(request, 'Sorry you are not allowed to broadcast, you have to first Login to apply for Broadcast', extra_tags='alert alert-warning alert-dismissible show')
		return redirect('accounts:login')

	# form = SignUpForm(request.POST)
	# if form.is_valid():
	# 	user = form.save()
	# 	user.refresh_from_db()
	# 	user.employee.first_name = form.cleaned_data.get('first_name')
	# 	user.employee.last_name = form.cleaned_data.get('last_name')
	# 	user.employee.email = form.cleaned_data.get('email')
	# 	user.save()
	# 	username = form.cleaned_data.get('username')
	# 	password = form.cleaned_data.get('password1')
	# 	user = authenticate(username=username, password=password)
	# 	login(request, user)
	# 	return redirect('accounts:login')
	# else:
	# 	form = SignUpForm()
	# return render(request, 'accounts/register.html', {'form': form,'profile': True})



def login_view(request):
	'''
	work on me - needs messages and redirects
	
	'''
	login_user = request.user
	if request.method == 'POST':
		form = UserLogin(data = request.POST)
		if form.is_valid():
			username = request.POST.get('username')
			password = request.POST.get('password')
			firstname = request.POST.get('firstname')
			lastname = request.POST.get('lastname')

			user = authenticate(request, username = username, password = password,firstname=firstname,lastname=lastname)
			if user and user.is_active:
				login(request,user)
				if login_user.is_staff:
					# return redirect('dashboard:dashboard11')
					return redirect('dashboard:dashboard')
				else:
					return redirect('dashboard:dashboard1')
			else:
			    messages.error(request,'Account is invalid',extra_tags = 'alert alert-error alert-dismissible show' )
			    return redirect('accounts:login')

		else:
			return HttpResponse('data not valid')

	dataset=dict()
	form = UserLogin()

	dataset['form'] = form
	return render(request,'accounts/login.html',dataset)


def user_profile_view(request):
	'''
	user profile view -> staffs (No edit) only admin/HR can edit.
	'''
	if not request.user.is_authenticated:
		return redirect('accounts:login')

	user = request.user
	employee = Employee.objects.filter(user = user).first()
	dataset = dict()
	dataset['user_detail'] = Details.objects.filter(user = user).first()
	dataset['employee'] = Employee.objects.filter(user = user).first()
	dataset['emergency'] = Emergency.objects.filter(employee = employee).first()
	dataset['family'] = Relationship.objects.filter(employee = employee).first()
	dataset['bank'] = Bank.objects.filter(employee = employee).first()
	return render(request,'dashboard/employee_detail.html',dataset)


def change_membership(request):
	if not request.user.is_authenticated:
		return redirect('accounts:login')

	user = request.user
	dataset = dict()
	dataset['employee'] = Employee.objects.filter(user=user).first()
	dataset['membership'] = Membership.objects.all()
	return render(request, 'accounts/membership_table.html', dataset)


def buy_membership(request):
	user = request.user
	if user.is_authenticated:
		employee = Employee.objects.filter(user=user).first()
		membership = Membership.objects.all()

		dataset = dict()
		dataset['employee'] = employee
		dataset['membership'] = membership

		return render(request, 'accounts/membership_table.html', dataset)
	return HttpResponse("Sorry , not authenticated for this,admin or whoever you are :)")


def logout_view(request):
	logout(request)
	return redirect('accounts:login')



def users_list(request):
	employees = Employee.objects.all()
	return render(request,'accounts/users_table.html',{'employees':employees,'title':'Users List'})


def users_unblock(request,id):
	user = get_object_or_404(User,id = id)
	emp = Employee.objects.filter(user = user).first()
	emp.is_blocked = False
	emp.save()
	user.is_active = True
	user.save()

	return redirect('accounts:users')


def users_block(request,id):
	user = get_object_or_404(User,id = id)
	emp = Employee.objects.filter(user = user).first()
	emp.is_blocked = True
	emp.save()
	
	user.is_active = False
	user.save()
	
	return redirect('accounts:users')



def users_blocked_list(request):
	blocked_employees = Employee.objects.all_blocked_employees()
	return render(request,'accounts/all_deleted_users.html',{'employees':blocked_employees,'title':'blocked users list'})