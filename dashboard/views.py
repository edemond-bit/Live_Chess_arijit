from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
import datetime
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
# from employee.forms import
from h5py._hl import dataset

from tournment.models import Leave, Players, Heats, Document, Content
from users.models import *
from tournment.forms import LeaveCreationForm, PlayerCreationForm, HeatsCreationForm, DocumentForm
# from leave.forms import CommentForm
import os


def dashboard(request):
    '''
    Summary of all apps - display here with charts etc.
    eg.lEAVE - PENDING|APPROVED|RECENT|REJECTED - TOTAL THIS MONTH or NEXT MONTH
    EMPLOYEE - TOTAL | GENDER
    CHART - AVERAGE EMPLOYEE AGES
    '''
    dataset = dict()
    user = request.user

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    employees = Employee.objects.all()
    leaves = Leave.objects.all_pending_leaves()
    # employees_birthday = Employee.objects.birthdays_current_month()
    staff_leaves = Leave.objects.filter(user=user)

    dataset['employees'] = employees
    dataset['leaves'] = leaves
    # dataset['employees_birthday'] = employees_birthday
    dataset['staff_leaves'] = staff_leaves
    dataset['title'] = 'summary'

    return render(request, 'dashboard/dashboard_index.html', dataset)

def dashboard_employees(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    dataset = dict()
    departments = Department.objects.all()
    employees = Employee.objects.all()

    # pagination
    query = request.GET.get('search')
    if query:
        employees = employees.filter(
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query)
        )

    paginator = Paginator(employees, 10)  # show 10 employee lists per page

    page = request.GET.get('page')
    employees_paginated = paginator.get_page(page)

    dataset['employee_list'] = employees_paginated
    dataset['departments'] = departments
    dataset['all_employees'] = Employee.objects.all_employees()

    blocked_employees = Employee.objects.all_blocked_employees()

    dataset['blocked_employees'] = blocked_employees
    dataset['title'] = 'Employees list view'
    return render(request, 'dashboard/employee_app.html', dataset)


def dashboard_user_create(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == 'POST':
        user = request.user
        if Details.objects.filter(user=user).exists():
            detail = Details.objects.get(user=user)
        else:
            detail = Details()
        detail.user = user
        detail.age = request.POST['age']
        detail.bio = request.POST['bio']
        detail.gender = request.POST['gender']
        detail.contact = request.POST['contact']
        if request.POST['dob'] != "":
            detail.dob = request.POST['dob']
        if 'image' in request.FILES:
            detail.image = request.FILES['image']
            # messages.error(request, 'Please upload',
            #                extra_tags='alert alert-warning alert-dismissible show')
            # return redirect('dashboard:usercreate')
        detail.save()
        messages.success(request, 'Details Uploaded successful',
                         extra_tags='alert alert-success alert-dismissible show')
        return redirect('accounts:userprofile')
    user = request.user
    dataset = dict()
    if Details.objects.filter(user=user).exists():
        user_detail = Details.objects.get(user=user)
        form = DetailForm(request.POST or None, instance=user_detail)
    else:
        form = DetailForm(request.POST or None)
    dataset['form'] = form
    dataset['title'] = 'User Personal Info'
    return render(request, 'dashboard/user_create.html', dataset)


def dashboard_employees_create(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            user = request.POST.get('user')
            assigned_user = User.objects.get(id=user)

            instance.user = assigned_user

            # instance.title = request.POST.get('title')
            instance.image = request.FILES.get('image')
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            # instance.othername = request.POST.get('othername')
            instance.sex = request.POST.get('sex')
            # instance.bio = request.POST.get('bio')
            # instance.birthday = request.POST.get('birthday')

            # religion_id = request.POST.get('religion')
            # religion = Religion.objects.get(id = religion_id)
            # instance.religion = religion

            # nationality_id = request.POST.get('nationality')
            # nationality = Nationality.objects.get(id = nationality_id)
            # instance.nationality = nationality

            # department_id = request.POST.get('department')
            # department = Department.objects.get(id = department_id)
            # instance.department = department

            # instance.hometown = request.POST.get('hometown')
            # instance.region = request.POST.get('region')
            # instance.residence = request.POST.get('residence')
            # instance.address = request.POST.get('address')
            # instance.education = request.POST.get('education')
            # instance.lastwork = request.POST.get('lastwork')
            # instance.position = request.POST.get('position')
            # instance.ssnitnumber = request.POST.get('ssnitnumber')
            # instance.tinnumber = request.POST.get('tinnumber')

            # role = request.POST.get('role')
            # role_instance = Role.objects.get(id = role)
            # instance.role = role_instance

            # instance.startdate = request.POST.get('startdate')
            # instance.employeetype = request.POST.get('employeetype')
            # instance.employeeid = request.POST.get('employeeid')
            # instance.dateissued = request.POST.get('dateissued')

            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()

            # employee_email = instance.user.email
            # email_subject = 'Humanly Access Credentials'
            # email_message = 'You have been added to Rabotecgroup Staff List,username and password'
            # from_email = settings.EMAIL_HOST_USER
            # to_email = [employee_email]
            '''
            Work on it - user@gmail.com & user@rabotecgroup.com -> send Template
            '''
            # send_mail(
            # 	email_subject,
            # 	email_message,
            # 	from_email,
            # 	to_email,
            # 	fail_silently=True
            # 	)

            # Send email - username & password to employee, how to get users decrypted password ?

            return redirect('dashboard:employees')
        else:
            messages.error(request, 'Trying to create dublicate employees with a single user account ',
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:employeecreate')

    dataset = dict()
    form = EmployeeCreateForm()
    dataset['form'] = form
    dataset['title'] = 'register employee'
    return render(request, 'dashboard/employee_create.html', dataset)


def employee_edit_data(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST or None, request.FILES or None, instance=employee)
        if form.is_valid():
            instance = form.save(commit=False)

            user = request.POST.get('user')
            assigned_user = User.objects.get(id=user)

            instance.user = assigned_user

            instance.title = request.POST.get('title')
            instance.image = request.FILES.get('image')
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            instance.othername = request.POST.get('othername')
            # instance.sex = request.POST.get('sex')
            # instance.bio = request.POST.get('bio')
            # instance.birthday = request.POST.get('birthday')

            # religion_id = request.POST.get('religion')
            # religion = Religion.objects.get(id = religion_id)
            # instance.religion = religion

            # nationality_id = request.POST.get('nationality')
            # nationality = Nationality.objects.get(id = nationality_id)
            # instance.nationality = nationality

            # department_id = request.POST.get('department')
            # department = Department.objects.get(id = department_id)
            # instance.department = department

            # instance.hometown = request.POST.get('hometown')
            # instance.region = request.POST.get('region')
            # instance.residence = request.POST.get('residence')
            # instance.address = request.POST.get('address')
            # instance.education = request.POST.get('education')
            # instance.lastwork = request.POST.get('lastwork')
            # instance.position = request.POST.get('position')
            # instance.ssnitnumber = request.POST.get('ssnitnumber')
            # instance.tinnumber = request.POST.get('tinnumber')

            # role = request.POST.get('role')
            # role_instance = Role.objects.get(id = role)
            # instance.role = role_instance

            # instance.startdate = request.POST.get('startdate')
            # instance.employeetype = request.POST.get('employeetype')
            # instance.employeeid = request.POST.get('employeeid')
            # instance.dateissued = request.POST.get('dateissued')

            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()
            messages.success(request, 'Account Updated Successfully !!!',
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:employees')

        else:

            messages.error(request, 'Error Updating account', extra_tags='alert alert-warning alert-dismissible show')
            return HttpResponse("Form data not valid")

    dataset = dict()
    form = EmployeeCreateForm(request.POST or None, request.FILES or None, instance=employee)
    dataset['form'] = form
    dataset['title'] = 'edit - {0}'.format(employee.get_full_name)
    return render(request, 'dashboard/employee_create.html', dataset)


def dashboard_employee_info(request, id):
    if not request.user.is_authenticated:
        return redirect('/')

    employee = get_object_or_404(Employee, id=id)
    employee_emergency_instance = Emergency.objects.filter(employee=employee).first()
    employee_family_instance = Relationship.objects.filter(employee=employee).first()
    bank_instance = Bank.objects.filter(employee=employee).first()

    dataset = dict()
    dataset['employee'] = employee
    dataset['emergency'] = employee_emergency_instance
    dataset['family'] = employee_family_instance
    dataset['bank'] = bank_instance
    dataset['title'] = 'profile - {0}'.format(employee.get_full_name)
    return render(request, 'dashboard/employee_detail.html', dataset)


# ------------------------- EMERGENCY --------------------------------


def dashboard_emergency_create(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    if request.method == 'POST':
        form = EmergencyCreateForm(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            employee_id = request.POST.get('employee')

            employee_object = Employee.objects.get(id=employee_id)
            emp_name = employee_object.get_full_name

            instance.employee = employee_object
            instance.fullname = request.POST.get('fullname')
            instance.tel = request.POST.get('tel')
            instance.location = request.POST.get('location')
            instance.relationship = request.POST.get('relationship')

            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()

            messages.success(request, 'Emergency Successfully Created for {0}'.format(emp_name),
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:emergencycreate')

        else:
            messages.error(request, 'Error Creating Emergency for {0}'.format(emp_name),
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:emergencycreate')

    dataset = dict()
    form = EmergencyCreateForm()
    dataset['form'] = form
    dataset['title'] = 'Create Emergency'
    return render(request, 'dashboard/emergency_create.html', dataset)


def dashboard_emergency_update(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('/')

    emergency = get_object_or_404(Emergency, id=id)
    employee = emergency.employee
    if request.method == 'POST':
        form = EmergencyCreateForm(data=request.POST, instance=emergency)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = employee
            instance.fullname = request.POST.get('fullname')
            instance.tel = request.POST.get('tel')
            instance.location = request.POST.get('location')
            instance.relationship = request.POST.get('relationship')

            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()

            messages.success(request, 'Emergency Details Successfully Updated',
                             extra_tags='alert alert-success alert-dismissible show')
            '''
                NB: redirect() will try to use its given arguments to reverse a URL. 
                This example assumes your URL patterns contain a pattern like this 
                redirect(assumed_url_name,its_assuemed_whatever_instance id)
            '''
            return redirect('dashboard:employeeinfo',
                            id=employee.id)  # worked on redirect to profile and message success and error

    dataset = dict()
    form = EmergencyCreateForm(request.POST or None, instance=emergency)
    dataset['form'] = form
    dataset['title'] = 'Updating Emergency Details for {0}'.format(employee.get_full_name)
    return render(request, 'dashboard/emergency_create.html', dataset)


# ----------------------------- FAMILY ---------------------------------#


# YOU ARE HERE ---- creation form for Family
def dashboard_family_create(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    if request.method == 'POST':
        form = FamilyCreateForm(data=request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            employee_id = request.POST.get('employee')
            employee_object = get_object_or_404(Employee, id=employee_id)
            instance.employee = employee_object
            instance.status = request.POST.get('status')
            instance.spouse = request.POST.get('spouse')
            instance.occupation = request.POST.get('occupation')
            instance.tel = request.POST.get('tel')
            instance.children = request.POST.get('children')
            instance.father = request.POST.get('father')
            instance.foccupation = request.POST.get('foccupation')
            instance.mother = request.POST.get('mother')
            instance.moccupation = request.POST.get('moccupation')

            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()

            messages.success(request, 'Relationship Successfully Created for {0}'.format(employee_object),
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:familycreate')
        else:
            messages.error(request, 'Failed to create Relationship for {0}'.format(employee_object),
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:familycreate')

    dataset = dict()

    form = FamilyCreateForm()

    dataset['form'] = form
    dataset['title'] = 'RELATIONSHIP CREATE FORM'
    return render(request, 'dashboard/family_create_form.html', dataset)


# HERE FAMILY EDIT
def dashboard_family_edit(request, id):
    if not (request.user.is_authenticated and request.user.is_authenticated):
        return redirect('/')
    relation = get_object_or_404(Relationship, id=id)
    employee = relation.employee

    # submitted form - bound form
    if request.method == 'POST':
        form = FamilyCreateForm(data=request.POST, instance=relation)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = employee
            instance.status = request.POST.get('status')
            instance.spouse = request.POST.get('spouse')
            instance.occupation = request.POST.get('occupation')
            instance.tel = request.POST.get('tel')
            instance.children = request.POST.get('children')

            # Recently added 29/03/19
            instance.nextofkin = request.POST.get('nextofkin')
            instance.contact = request.POST.get('contact')
            instance.relationship = request.POST.get('relationship')

            instance.father = request.POST.get('father')
            instance.foccupation = request.POST.get('foccupation')
            instance.mother = request.POST.get('mother')
            instance.moccupation = request.POST.get('moccupation')

            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()

            messages.success(request, 'Relationship Successfully Updated for {0}'.format(employee.get_full_name),
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:familycreate')

        else:
            messages.error(request, 'Failed to update Relationship for {0}'.format(employee.get_full_name),
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:familycreate')

    dataset = dict()

    form = FamilyCreateForm(request.POST or None, instance=relation)

    dataset['form'] = form
    dataset['title'] = 'RELATIONSHIP UPDATE FORM'
    return render(request, 'dashboard/family_create_form.html', dataset)


# BANK

def dashboard_bank_create(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    if request.method == 'POST':
        form = BankAccountCreation(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            employee_id = request.POST.get('employee')
            employee_object = get_object_or_404(Employee, id=employee_id)

            instance.employee = employee_object
            instance.name = request.POST.get('name')
            instance.branch = request.POST.get('branch')
            instance.account = request.POST.get('account')
            instance.salary = request.POST.get('salary')

            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()

            messages.success(request, 'Account Successfully Created for {0}'.format(employee_object.get_full_name),
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:bankaccountcreate')
        else:
            messages.error(request, 'Error Creating Account for {0}'.format(employee_object.get_full_name),
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:bankaccountcreate')

    dataset = dict()

    form = BankAccountCreation()

    dataset['form'] = form
    dataset['title'] = 'Account Creation Form'
    return render(request, 'dashboard/bank_account_create_form.html', dataset)


def employee_bank_account_update(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    bank_instance_obj = get_object_or_404(Bank, id=id)
    employee = bank_instance_obj.employee

    if request.method == 'POST':
        form = BankAccountCreation(request.POST, instance=bank_instance_obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = employee

            instance.name = request.POST.get('name')
            instance.branch = request.POST.get('branch')
            instance.account = request.POST.get('account')
            instance.salary = request.POST.get('salary')

            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()

            messages.success(request, 'Account Successfully Edited for {0}'.format(employee.get_full_name),
                             extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:bankaccountcreate')
        else:
            messages.error(request, 'Error Updating Account for {0}'.format(employee.get_full_name),
                           extra_tags='alert alert-warning alert-dismissible show')
            return redirect('dashboard:bankaccountcreate')

    dataset = dict()

    form = BankAccountCreation(request.POST or None, instance=bank_instance_obj)

    dataset['form'] = form
    dataset['title'] = 'Update Bank Account'
    return render(request, 'dashboard/bank_account_create_form.html', dataset)


# ---------------------LEAVE-------------------------------------------


def leave_creation(request):
    if request.user.is_authenticated:
        if (request.user.employee.membership.level == 0) or (request.user.employee.membership.level == 2):
            messages.error(request, 'Buy Membership to avail this offer.',
                           extra_tags='alert alert-danger alert-dismissible show')
            return redirect('accounts:buymembership')
        if request.method == 'POST':
            if 'id' in request.POST:
                id = request.POST['id']
            else:
                id = ""
            if id != "":
                leave = Leave.objects.get(id=id)
                message = 'Tournament updated successfully'
            else:
                leave = Leave()
                leave.user = request.user
                message = 'Tournament created successfully'
            leave.name = request.POST['name']
            leave.desc = request.POST['desc']
            leave.location = request.POST['location']
            leave.type = request.POST['type']
            leave.country = request.POST['country']
            leave.laws = request.POST['laws']
            leave.startdate = request.POST['startdate']
            leave.starttime = request.POST['starttime']
            leave.enddate = request.POST['enddate']
            leave.endtime = request.POST['endtime']
            leave.timezone = request.POST['timezone']
            leave.rounds = request.POST['rounds']
            leave.save()
            print()

            messages.success(request, message, extra_tags='alert alert-success alert-dismissible show')
            return redirect('dashboard:userleaveedit', id=leave.id)
    else:
        return redirect('accounts:login')


# def leave_creation(request):


# 	if request.method == 'POST':
# 		form = LeaveCreationForm(data = request.POST)
# 		cform = CommentForm(data = request.POST)
# 		if form.is_valid() and cform.is_valid():
# 			instance = form.save(commit = False)
# 			user = request.user
# 			instance.user = user
# 			instance.save()
# 			print(instance)

# 			# Commment form save  logic
# 			comment_inst = cform.save(commit = False)
# 			# comment_inst.leave = instance
# 			# comment_inst.comment = request.POST['comment']
# 			cinstance.save()

# 			return HttpResponse('success')

# 		else:
# 			return HttpResponse('error')


# 	dataset = dict()

# 	form = LeaveCreationForm()
# 	cform = CommentForm() 
# 	dataset['form'] = form
# 	dataset['cform'] = cform
# 	return render(request,'dashboard/create_leave.html',dataset)


def leaves_list(request):
    if not (request.user.is_staff and request.user.is_superuser):
        return redirect('/')
    leaves = Leave.objects.all_pending_leaves()
    return render(request, 'dashboard/leaves_recent.html', {'leave_list': leaves, 'title': 'leaves list - pending'})


def leaves_approved_list(request):
    if not (request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    leaves = Leave.objects.all_approved_leaves()  # approved leaves -> calling model manager method
    return render(request, 'dashboard/leaves_approved.html', {'leave_list': leaves, 'title': 'approved leave list'})


def leaves_view(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if (request.user.employee.membership.level == 0) or (request.user.employee.membership.level == 2):
        messages.error(request, 'Buy Membership to avail this offer.',
                       extra_tags='alert alert-danger alert-dismissible show')
        return redirect('accounts:buymembership')

    leave = get_object_or_404(Leave, id=id)
    employee = Employee.objects.filter(user=leave.user)[0]
    print(employee)
    return render(request, 'dashboard/leave_detail_view.html', {'leave': leave, 'employee': employee,
                                                                'title': '{0}-{1} leave'.format(leave.user.username,
                                                                                                leave.status)})


from django import forms
from django.forms.models import inlineformset_factory


def leaves_edit(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if (request.user.employee.membership.level == 0) or (request.user.employee.membership.level == 2):
        messages.error(request, 'Buy Membership to avail this offer.',
                       extra_tags='alert alert-danger alert-dismissible show')
        return redirect('accounts:buymembership')
    leave = get_object_or_404(Leave, pk=id)
    HeatFormSet = inlineformset_factory(Leave, Heats, form=HeatsCreationForm, extra=1)
    PlayerFormSet = inlineformset_factory(Leave, Players, form=PlayerCreationForm, extra=1, max_num=1000)
    DocumentFormSet = inlineformset_factory(Leave, Document, form=DocumentForm, extra=1,
                                            widgets={
                                               'rounds': forms.Select(
                                                   choices=[("Round-" + str(i), "Round-" + str(i)) for i in
                                                            range(1, (int(Leave.objects.get(pk=id).rounds) + 1))]),
                                               'games': forms.Select(choices=[(str(heat.player1) + "_vs_" + str(
                                                   heat.player2), str(heat.player1) + "_vs_" + str(heat.player2))
                                                                              for heat in Heats.objects.filter(tournment=id)])
                                           })

    dataset = dict()
    form = LeaveCreationForm(request.POST or None, instance=leave)
    form1 = PlayerFormSet(instance=leave)
    formset = HeatFormSet(instance=leave)
    for f in formset:
        f.fields['player1'].queryset = Players.objects.filter(tournment=id)
        f.fields['player2'].queryset = Players.objects.filter(tournment=id)
    formset1 = DocumentFormSet(instance=leave)
    dataset['form'] = form
    dataset['form1'] = form1
    dataset['formset'] = formset
    dataset['formset1'] = formset1

    dataset['title'] = 'Tournament Details'
    dataset['flag'] = 3
    dataset['id'] = id
    return render(request, 'dashboard/create_player.html', dataset)


def approve_leave(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leave = get_object_or_404(Leave, id=id)
    user = leave.user
    employee = Employee.objects.filter(user=user)[0]
    leave.approve_leave

    messages.error(request, 'Tournment successfully approved for {0}'.format(employee.get_full_name),
                   extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:userleaveview', id=id)


def cancel_leaves_list(request):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leaves = Leave.objects.all_cancel_leaves()
    return render(request, 'dashboard/leaves_cancel.html', {'leave_list_cancel': leaves, 'title': 'Cancel leave list'})


def unapprove_leave(request, id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('/')
    leave = get_object_or_404(Leave, id=id)
    leave.unapprove_leave
    return redirect('dashboard:leaveslist')  # redirect to unapproved list


def cancel_leave(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leave = get_object_or_404(Leave, id=id)
    leave.leaves_cancel

    messages.success(request, 'Tournment is canceled', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:canceleaveslist')  # work on redirecting to instance leave - detail view


# Current section -> here
def uncancel_leave(request, id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leave = get_object_or_404(Leave, id=id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()
    messages.success(request, 'Tournment is uncanceled,now in pending list',
                     extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:canceleaveslist')  # work on redirecting to instance leave - detail view


def leave_rejected_list(request):
    dataset = dict()
    leave = Leave.objects.all_rejected_leaves()

    dataset['leave_list_rejected'] = leave
    return render(request, 'dashboard/rejected_leaves_list.html', dataset)


def reject_leave(request, id):
    dataset = dict()
    leave = get_object_or_404(Leave, id=id)
    leave.reject_leave
    messages.success(request, 'Tournment is rejected', extra_tags='alert alert-success alert-dismissible show')
    return redirect('dashboard:leavesrejected')

    # return HttpResponse(id)


def unreject_leave(request, id):
    leave = get_object_or_404(Leave, id=id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()
    messages.success(request, 'Tournment is now in pending list ',
                     extra_tags='alert alert-success alert-dismissible show')

    return redirect('dashboard:leavesrejected')


# Rabotec staffs leaves table user only
def view_my_leave_table(request):
    # work on the logics
    if request.user.is_authenticated:
        if (request.user.employee.membership.level == 0) or (request.user.employee.membership.level == 2):
            messages.error(request, 'Buy Membership to avail this offer.',
                           extra_tags='alert alert-danger alert-dismissible show')
            return redirect('accounts:buymembership')
        user = request.user
        leaves = Leave.objects.filter(user=user)
        employee = Employee.objects.filter(user=user).first()
        dataset = dict()
        dataset['leave_list'] = leaves
        dataset['employee'] = employee
        dataset['title'] = 'Leaves List'
    else:
        return redirect('accounts:login')
    return render(request, 'dashboard/staff_leaves_table.html', dataset)


def admin_tournment_table(request):
    # work on the logics
    if request.user.is_superuser:
        # user = request.user
        leaves = Leave.objects.all()
        # employee = Employee.objects.filter(user = user).first()
        # print(leaves)
        dataset = dict()
        dataset['leave_list'] = leaves
        # dataset['employee'] = employee
        dataset['title'] = 'Leaves List'
    else:
        return redirect('accounts:login')
    return render(request, 'dashboard/admin_tournment_table.html', dataset)


# Birthday
def birthday_this_month(request):
    if not request.user.is_authenticated:
        return redirect('/')

    employees = Employee.objects.birthdays_current_month()
    month = datetime.date.today().strftime(
        '%B')  # am using this to get the month for template rendering- making it dynamic
    context = {
        'birthdays': employees,
        'month': month,
        'count_birthdays': employees.count(),
        'title': 'Birthdays'
    }
    return render(request, 'dashboard/birthdays_this_month.html', context)


def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    dataset = dict()
    user = request.user
    employee = Employee.objects.filter(user=user).first()
    leaves = Leave.objects.filter(user=user, is_approved=True)
    dataset['leave_list'] = leaves
    dataset['employee'] = employee
    return render(request, 'dashboard/user_dashboard.html', dataset)


def dashboard_view_analysis(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if (request.user.employee.membership.level == 0) or (request.user.employee.membership.level == 1):
        messages.error(request, 'Buy Membership to avail this offer.',
                       extra_tags='alert alert-danger alert-dismissible show')
        return redirect('accounts:buymembership')
    dataset1 = dict()
    item = {}
    doc_list = []

    document = get_object_or_404(Document, pk=id)
    leave = get_object_or_404(Leave, id=int(document.tournament.id))
    file_name = leave.user.username + "_" + document.games
    file_loc = os.path.join(settings.BASE_DIR, 'media', (leave.user.username + "--" + leave.name),
                            document.rounds, document.games, (file_name + ".pgn"))
    item['id'] = document.id
    item['tournament'] = document.tournament
    item['round'] = document.rounds
    x = document.games.split("_vs_")
    item['player1'] = x[0]
    item['player2'] = x[1]
    doc_list.append(item)
    with open(file_loc, 'r') as reader:
        s = reader.read()
    dataset1['content'] = [{'content': s}]
    dataset1['heats'] = doc_list
    dataset1['id'] = id
    print(dataset1)
    return render(request, 'app/dashboard1.html', dataset1)


def test2(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    dataset = dict()
    doc_list = []
    tournament = None
    leave = get_object_or_404(Leave, id=id)
    documents = Document.objects.filter(tournament=leave.id)
    for document in documents:
        item = {}
        item['id'] = document.id
        tournament = document.tournament
        item['round'] = document.rounds
        x = document.games.split("_vs_")
        item['player1'] = x[0]
        item['player2'] = x[1]
        doc_list.append(item)
    dataset['document'] = doc_list
    dataset['tournament'] = tournament
    return render(request, 'app/test2.html', dataset)


def dashboard_view1(request, id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    dataset = dict()
    doc_list = []
    item = {}
    document = get_object_or_404(Document, pk=id)
    leave = get_object_or_404(Leave, id=int(document.tournament.id))
    file_name = leave.user.username + "_" + document.games
    file_loc = os.path.join(settings.BASE_DIR, 'media', (leave.user.username + "--" + leave.name),
                            document.rounds, document.games, (file_name + ".pgn"))
    item['id'] = document.id
    item['tournament'] = document.tournament
    item['round'] = document.rounds
    x = document.games.split("_vs_")
    item['player1'] = x[0]
    item['player2'] = x[1]
    if request.user == leave.user:
        item['loc'] = document.loc
    doc_list.append(item)
    if os.path.isfile(file_loc):
        with open(file_loc, 'r') as reader:
            s = reader.read()
    else:
        s = ""
    dataset['content'] = [{'content': s}]
    dataset['document'] = doc_list
    print(dataset)
    return render(request, 'app/dashboard.html', dataset)


def test4(request):
    return render(request, 'app/test4.html')


def broadcast(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        # handle_uploaded_file(request.FILES['docfile'], str(request.FILES['docfile']))
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            options = []
            with open('media/documents/game-1.pgn', 'r') as reader:
                # for line in reader:
                #     currentPlace = line[:-1]
                #     options.append(currentPlace)
                #     print(options)
                s = reader.read()
                myobject = Content(content=s)
                myobject.save()

            # Redirect to the document list after POST
            return redirect('dashboard:broadcast')
            # return HttpResponseRedirect(reverse('users:list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    content = Content.objects.all()
    # Render list page with the documents and the form
    return render(request, 'app/list.html', {'documents': documents, 'content': content, 'form': form})


from pathlib import Path
import shutil
from cron import cron_job


def uploadpgn(request):
    if not request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    if (request.user.employee.membership.level == 0) or (request.user.employee.membership.level == 2):
        messages.error(request, 'Buy Membership to avail this offer.',
                       extra_tags='alert alert-danger alert-dismissible show')
        return redirect('accounts:buymembership')
    # form = DocumentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        # if not form.is_valid():
        #     return render(request, 'dashboard/create_player.html', {'form': form})
        for i in range(int(request.POST['document_set-TOTAL_FORMS'])):
            if 'document_set-' + str(i) + '-id' in request.POST:
                if 'document_set-' + str(i) + '-DELETE' in request.POST:
                    if request.POST['document_set-' + str(i) + '-DELETE'] == 'on':
                        if request.POST['document_set-' + str(i) + '-id'] != "":
                            id = int(request.POST['document_set-' + str(i) + '-id'])
                            if Document.objects.filter(id=id).exists():
                                Document.objects.get(id=id).delete()
                        continue
            if "document_set-" + str(i) + "-id" in request.POST:
                if request.POST["document_set-" + str(i) + "-id"] != "":
                    id = request.POST["document_set-" + str(i) + "-id"]
                    document = Document.objects.get(pk=id)
                else:
                    document = Document()
                # if request.POST["document_set-" + str(i) + "-loc"] == "":
                #     messages.error(request, 'Please Enter PGN File Location',
                #                    extra_tags='alert alert-danger alert-dismissible show')
                #     return redirect(request.META.get('HTTP_REFERER'))
                # else:
                    # if os.path.isfile(request.POST["document_set-" + str(i) + "-loc"]):
                    #     pass
                    # else:
                    #     messages.error(request, 'PGN File Location you entered is not a valid file location',
                    #                    extra_tags='alert alert-danger alert-dismissible show')
                    #     return redirect(request.META.get('HTTP_REFERER'))
                if request.POST["pgn_id"] != "":
                    document.tournament = Leave.objects.get(pk=request.POST["pgn_id"])
                else:
                    messages.error(request, 'You are trying to add without adding tournament first',
                                   extra_tags='alert alert-danger alert-dismissible show')
                document.rounds = request.POST["document_set-" + str(i) + "-rounds"]
                document.games = request.POST["document_set-" + str(i) + "-games"]
                # document.loc = request.POST["document_set-" + str(i) + "-loc"]
                if "document_set-" + str(i) + "-docfile" in request.FILES:
                    document.docfile = request.FILES["document_set-" + str(i) + "-docfile"]
                print(document.docfile)
                if not document.docfile:
                    messages.error(request, 'Pgn not selected',
                                     extra_tags='alert alert-danger alert-dismissible show')
                    return redirect(request.META.get('HTTP_REFERER'))
                document.save()
                file_name = request.user.username + "_" + document.games
                loc = os.path.join(settings.BASE_DIR, 'media', request.user.username + "--"
                                   + document.tournament.name, document.rounds, document.games)
                Path(loc).mkdir(parents=True, exist_ok=True)
                # fileitem = request.POST["document_set-" + str(i) + "-loc"]
                fileitem = document.docfile
                print(fileitem)
                print(os.path.join(settings.MEDIA_ROOT, fileitem.name))
                file_loc = os.path.join(settings.BASE_DIR, 'media', request.user.username
                                        + "--" + document.tournament.name, document.rounds,
                                        document.games, file_name + ".pgn")
                with open(os.path.join(settings.MEDIA_ROOT, fileitem.name), "rb") as source:
                    with open(file_loc, "wb") as destination:
                        for line in source:
                            destination.write(line)
                # cron_job.start(loc, file_name, fileitem)
        messages.success(request, 'Pgn upload successfully', extra_tags='alert alert-success alert-dismissible show')
        return redirect(request.META.get('HTTP_REFERER'))


from django.shortcuts import render
from django.contrib.auth import login, authenticate
from users.forms import SignUpForm, DetailForm
from django.shortcuts import render, redirect


def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.employee.first_name = form.cleaned_data.get('first_name')
        user.employee.last_name = form.cleaned_data.get('last_name')
        user.employee.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('dashboard:register')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})


def player_creation(request):
    if request.user.is_authenticated:
        if (request.user.employee.membership.level == 0) or (request.user.employee.membership.level == 2):
            messages.error(request, 'Buy Membership to avail this offer.',
                           extra_tags='alert alert-danger alert-dismissible show')
            return redirect('accounts:buymembership')
        if request.method == 'POST':
            print(request.POST)
            tournament_id = request.POST['player_id']
            for i in range(int(request.POST['players_set-TOTAL_FORMS'])):
                if 'players_set-' + str(i) + '-id' in request.POST:
                    if 'players_set-' + str(i) + '-DELETE' in request.POST:
                        if request.POST['players_set-' + str(i) + '-DELETE'] == 'on':
                            if request.POST['players_set-' + str(i) + '-id'] != "":
                                id = int(request.POST['players_set-' + str(i) + '-id'])
                                Players.objects.get(id=id).delete()
                            continue
                    if request.POST['players_set-' + str(i) + '-id'] != "":
                        id = int(request.POST['players_set-' + str(i) + '-id'])
                        player = Players.objects.get(id=id)
                        message = 'Player updated successfully'
                    else:
                        player = Players()
                        player.user = request.user
                        player.tournment = Leave.objects.get(id=tournament_id)
                        message = 'Player created successfully'
                    if request.POST['players_set-' + str(i) + '-name'] != "":
                        player.name = request.POST['players_set-' + str(i) + '-name']
                    else:
                        messages.error(request, "Player name cannot be empty", extra_tags='alert alert-danger alert-dismissible show')
                        return redirect(request.META.get('HTTP_REFERER'))
                    player.last = request.POST['players_set-' + str(i) + '-last']
                    player.gender = request.POST['players_set-' + str(i) + '-gender']
                    if request.POST['players_set-' + str(i) + '-ranking'] != "":
                        player.ranking = int(request.POST['players_set-' + str(i) + '-ranking'])
                    if request.POST['players_set-' + str(i) + '-rating'] != "":
                        player.rating = int(request.POST['players_set-' + str(i) + '-rating'])
                    if request.POST['players_set-' + str(i) + '-COUNTRY_RATING'] != "":
                        player.COUNTRY_RATING = int(request.POST['players_set-' + str(i) + '-COUNTRY_RATING'])
                    player.title = request.POST['players_set-' + str(i) + '-title']
                    player.save()

            messages.success(request, message, extra_tags='alert alert-success alert-dismissible show')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('accounts:login')

def heats_creation(request):
    if request.user.is_authenticated:
        if (request.user.employee.membership.level == 0) or (request.user.employee.membership.level == 2):
            messages.error(request, 'Buy Membership to avail this offer.',
                           extra_tags='alert alert-danger alert-dismissible show')
            return redirect('accounts:buymembership')
        if request.method == 'POST':
            tournament_id = request.POST['heat_id']
            for i in range(int(request.POST['heats_set-TOTAL_FORMS'])):
                if 'heats_set-' + str(i) + '-id' in request.POST:
                    if request.POST['heats_set-' + str(i) + '-id'] != "":
                        id = int(request.POST['heats_set-' + str(i) + '-id'])
                        if 'heats_set-' + str(i) + '-DELETE' in request.POST:
                            if request.POST['heats_set-' + str(i) + '-DELETE'] == 'on':
                                Heats.objects.get(id=id).delete()
                                continue
                        heat = Heats.objects.get(id=id)
                        message = 'Rounds updated successfully'
                    else:
                        heat = Heats()
                        heat.user = request.user
                        heat.tournment = Leave.objects.get(id=tournament_id)
                        message = 'Rounds created successfully'
                    if request.POST['heats_set-' + str(i) + '-rounds'] != "":
                        heat.rounds = request.POST['heats_set-' + str(i) + '-rounds']
                    else:
                        message = 'Rounds player per round field is required updated successfully'
                    heat.player1 = Players.objects.get(id=request.POST['heats_set-' + str(i) + '-player1'])
                    heat.player2 = Players.objects.get(id=request.POST['heats_set-' + str(i) + '-player2'])
                    heat.save()

            messages.success(request, message, extra_tags='alert alert-success alert-dismissible show')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('accounts:login')


def heats(request, id):
    print("create opponents view here")
    if not request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    ls = Leave.objects.get(id=id)

    if ls in request.user.user.all():

        if request.method == 'POST':
            form = HeatsCreationForm(data=request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                user = request.user
                instance.user = user
                instance.save()

                messages.success(request, 'Opponents created sucessfully',
                                 extra_tags='alert alert-success alert-dismissible show')

    dataset = dict()
    form = HeatsCreationForm()
    dataset['form'] = form
    dataset['title'] = 'Create Rounds'
    return render(request, 'dashboard/create_leave.html', dataset)


def leave_creation1(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if (request.user.employee.membership.level == 0) or (request.user.employee.membership.level == 2):
        messages.error(request, 'Buy Membership to avail this offer.',
                       extra_tags='alert alert-danger alert-dismissible show')
        return redirect('accounts:buymembership')
    HeatFormSet = inlineformset_factory(Leave, Heats, form=HeatsCreationForm, extra=1)
    PlayerFormSet = inlineformset_factory(Leave, Players, form=PlayerCreationForm, extra=1, max_num=1000)

    dataset = dict()
    form = LeaveCreationForm(request.POST or None)
    form1 = PlayerFormSet()
    formset = HeatFormSet()
    # for f in formset:
    #     f.fields['player1'].queryset = Players.objects.filter(tournment=id)
    #     f.fields['player2'].queryset = Players.objects.filter(tournment=id)
    dataset['form'] = form
    dataset['form1'] = form1
    dataset['formset'] = formset

    dataset['title'] = 'Tournament Details'
    dataset['flag'] = 2
    return render(request, 'dashboard/create_player.html', dataset)
