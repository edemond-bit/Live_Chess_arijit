from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
import datetime
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
# from employee.forms import
from h5py._hl import dataset

from tournment.models import Leave,Players,Heats,Document,Content
from users.models import *
from tournment.forms import LeaveCreationForm,PlayerCreationForm,HeatsCreationForm,DocumentForm
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
    staff_leaves = Leave.objects.filter(user = user)


    dataset['employees'] = employees
    dataset['leaves'] = leaves
    # dataset['employees_birthday'] = employees_birthday
    dataset['staff_leaves'] = staff_leaves
    dataset['title'] = 'summary'


    return render(request,'dashboard/dashboard_index.html',dataset)




def dashboard_employees(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    dataset = dict()
    departments = Department.objects.all()
    employees = Employee.objects.all()

    #pagination
    query = request.GET.get('search')
    if query:
        employees = employees.filter(
            Q(firstname__icontains = query) |
            Q(lastname__icontains = query)
        )



    paginator = Paginator(employees, 10) #show 10 employee lists per page

    page = request.GET.get('page')
    employees_paginated = paginator.get_page(page)


    dataset['employee_list'] = employees_paginated
    dataset['departments'] = departments
    dataset['all_employees'] = Employee.objects.all_employees()

    blocked_employees = Employee.objects.all_blocked_employees()

    dataset['blocked_employees'] = blocked_employees
    dataset['title'] = 'Employees list view'
    return render(request,'dashboard/employee_app.html',dataset)



def dashboard_user_create(request):


    if request.method == 'POST':
        form = DetailForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            user = request.user
            assigned_user = user



            instance.user = assigned_user

            # instance.title = request.POST.get('title')
            instance.image = request.FILES.get('image')
            instance.firstname = request.POST.get('firstname')
            instance.lastname = request.POST.get('lastname')
            # instance.othername = request.POST.get('othername')
            instance.age = request.POST.get('age')
            instance.bio = request.POST.get('bio')
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

            #Send email - username & password to employee, how to get users decrypted password ?

            return  redirect('dashboard:employees')
        else:
            messages.error(request,'You are doing something wrong!!!! ',extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:employeecreate')


    dataset = dict()
    form = DetailForm()
    dataset['form'] = form
    dataset['title'] = 'User Personal Info'
    return render(request,'dashboard/user_create.html',dataset)
def dashboard_employees_create(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')

    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            user = request.POST.get('user')
            assigned_user = User.objects.get(id = user)

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

            #Send email - username & password to employee, how to get users decrypted password ?

            return  redirect('dashboard:employees')
        else:
            messages.error(request,'Trying to create dublicate employees with a single user account ',extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:employeecreate')


    dataset = dict()
    form = EmployeeCreateForm()
    dataset['form'] = form
    dataset['title'] = 'register employee'
    return render(request,'dashboard/employee_create.html',dataset)





def employee_edit_data(request,id):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    employee = get_object_or_404(Employee, id = id)
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST or None,request.FILES or None,instance = employee)
        if form.is_valid():
            instance = form.save(commit = False)

            user = request.POST.get('user')
            assigned_user = User.objects.get(id = user)

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
            messages.success(request,'Account Updated Successfully !!!',extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:employees')

        else:

            messages.error(request,'Error Updating account',extra_tags = 'alert alert-warning alert-dismissible show')
            return HttpResponse("Form data not valid")

    dataset = dict()
    form = EmployeeCreateForm(request.POST or None,request.FILES or None,instance = employee)
    dataset['form'] = form
    dataset['title'] = 'edit - {0}'.format(employee.get_full_name)
    return render(request,'dashboard/employee_create.html',dataset)






def dashboard_employee_info(request,id):
    if not request.user.is_authenticated:
        return redirect('/')

    employee = get_object_or_404(Employee, id = id)
    employee_emergency_instance = Emergency.objects.filter(employee = employee).first()
    employee_family_instance = Relationship.objects.filter(employee = employee).first()
    bank_instance = Bank.objects.filter(employee = employee).first()

    dataset = dict()
    dataset['employee'] = employee
    dataset['emergency'] = employee_emergency_instance
    dataset['family'] = employee_family_instance
    dataset['bank'] = bank_instance
    dataset['title'] = 'profile - {0}'.format(employee.get_full_name)
    return render(request,'dashboard/employee_detail.html',dataset)




# ------------------------- EMERGENCY --------------------------------


def dashboard_emergency_create(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    if request.method == 'POST':
        form = EmergencyCreateForm(data = request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            employee_id = request.POST.get('employee')

            employee_object = Employee.objects.get(id = employee_id)
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

            messages.success(request,'Emergency Successfully Created for {0}'.format(emp_name),extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:emergencycreate')

        else:
            messages.error(request,'Error Creating Emergency for {0}'.format(emp_name),extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:emergencycreate')

    dataset = dict()
    form = EmergencyCreateForm()
    dataset['form'] = form
    dataset['title'] = 'Create Emergency'
    return render(request,'dashboard/emergency_create.html',dataset)




def dashboard_emergency_update(request,id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('/')

    emergency = get_object_or_404(Emergency, id = id)
    employee = emergency.employee
    if request.method == 'POST':
        form = EmergencyCreateForm( data = request.POST, instance = emergency)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.employee = employee
            instance.fullname = request.POST.get('fullname')
            instance.tel = request.POST.get('tel')
            instance.location = request.POST.get('location')
            instance.relationship = request.POST.get('relationship')

            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()


            messages.success(request,'Emergency Details Successfully Updated',extra_tags = 'alert alert-success alert-dismissible show')
            '''
                NB: redirect() will try to use its given arguments to reverse a URL. 
                This example assumes your URL patterns contain a pattern like this 
                redirect(assumed_url_name,its_assuemed_whatever_instance id)
            '''
            return redirect('dashboard:employeeinfo',id = employee.id)# worked on redirect to profile and message success and error

    dataset = dict()
    form = EmergencyCreateForm(request.POST or None,instance = emergency)
    dataset['form'] = form
    dataset['title'] = 'Updating Emergency Details for {0}'.format(employee.get_full_name)
    return render(request,'dashboard/emergency_create.html',dataset)





# ----------------------------- FAMILY ---------------------------------#



# YOU ARE HERE ---- creation form for Family
def dashboard_family_create(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    if request.method == 'POST':
        form = FamilyCreateForm(data = request.POST or None)
        if form.is_valid():
            instance = form.save(commit = False)
            employee_id = request.POST.get('employee')
            employee_object = get_object_or_404(Employee,id = employee_id)
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

            messages.success(request,'Relationship Successfully Created for {0}'.format(employee_object),extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:familycreate')
        else:
            messages.error(request,'Failed to create Relationship for {0}'.format(employee_object),extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:familycreate')




    dataset = dict()

    form = FamilyCreateForm()

    dataset['form'] = form
    dataset['title'] = 'RELATIONSHIP CREATE FORM'
    return render(request,'dashboard/family_create_form.html',dataset)




# HERE FAMILY EDIT
def dashboard_family_edit(request,id):
    if not (request.user.is_authenticated and request.user.is_authenticated):
        return redirect('/')
    relation = get_object_or_404(Relationship, id = id)
    employee = relation.employee

    #submitted form - bound form
    if request.method == 'POST':
        form = FamilyCreateForm(data = request.POST, instance = relation)
        if form.is_valid():
            instance = form.save(commit = False)
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

            messages.success(request,'Relationship Successfully Updated for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:familycreate')

        else:
            messages.error(request,'Failed to update Relationship for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:familycreate')



    dataset = dict()

    form = FamilyCreateForm(request.POST or None,instance = relation)

    dataset['form'] = form
    dataset['title'] = 'RELATIONSHIP UPDATE FORM'
    return render(request,'dashboard/family_create_form.html',dataset)





# BANK 

def dashboard_bank_create(request):
    if not (request.user.is_authenticated and request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    if request.method == 'POST':
        form = BankAccountCreation(data = request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            employee_id = request.POST.get('employee')
            employee_object = get_object_or_404(Employee,id = employee_id)

            instance.employee = employee_object
            instance.name = request.POST.get('name')
            instance.branch = request.POST.get('branch')
            instance.account = request.POST.get('account')
            instance.salary = request.POST.get('salary')

            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()

            messages.success(request,'Account Successfully Created for {0}'.format(employee_object.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:bankaccountcreate')
        else:
            messages.error(request,'Error Creating Account for {0}'.format(employee_object.get_full_name),extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:bankaccountcreate')


    dataset = dict()

    form = BankAccountCreation()

    dataset['form'] = form
    dataset['title'] = 'Account Creation Form'
    return render(request,'dashboard/bank_account_create_form.html',dataset)








def employee_bank_account_update(request,id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    bank_instance_obj = get_object_or_404(Bank, id = id)
    employee = bank_instance_obj.employee

    if request.method == 'POST':
        form = BankAccountCreation(request.POST, instance = bank_instance_obj)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.employee = employee

            instance.name = request.POST.get('name')
            instance.branch = request.POST.get('branch')
            instance.account = request.POST.get('account')
            instance.salary = request.POST.get('salary')

            # now = datetime.datetime.now()
            # instance.created = now
            # instance.updated = now

            instance.save()

            messages.success(request,'Account Successfully Edited for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:bankaccountcreate')
        else:
            messages.error(request,'Error Updating Account for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-warning alert-dismissible show')
            return redirect('dashboard:bankaccountcreate')


    dataset = dict()

    form = BankAccountCreation(request.POST or None,instance = bank_instance_obj)

    dataset['form'] = form
    dataset['title'] = 'Update Bank Account'
    return render(request,'dashboard/bank_account_create_form.html',dataset)





# ---------------------LEAVE-------------------------------------------



def leave_creation(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    HeatFormSet = modelformset_factory(Heats,fields=('tournment','rounds','player1','player2') )
    if request.method == 'POST':
        form = LeaveCreationForm(data = request.POST)
        form1 = PlayerCreationForm(data = request.POST)
        form2 = HeatFormSet(data = request.POST)
        if form.is_valid() or form1.is_valid():

            instance = form.save(commit = False)
            user = request.user
            instance.user = user
            instance.name=request.POST.get('name')
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            BASE_DIR1 = os.path.dirname(BASE_DIR)
            BASE_DIR2 =os.path.dirname(BASE_DIR1)
            # Directory
            directory = str(user ) + "--" + str(instance.name)

            # Parent Directory path
            url= os.path.join(BASE_DIR1, 'media')

            # Path
            path = os.path.join(url, directory)

            # Create the directory

            os.mkdir(path)
            print("Directory '% s' created" % directory)
            instance.rounds=request.POST.get('rounds')
            x=int(instance.rounds)
            # print('hdfahsgcvaskhcgashgcasihckashc',x)
            for i in range(1,x+1) :
                directory1 = "round-"+ str(i)

                path1 = os.path.join(path, directory1)
                os.mkdir(path1)
                # print(directory1)

            instance.save()


            # print(instance.defaultdays)
            messages.success(request,'Tournment first part is completed',extra_tags = 'alert alert-success alert-dismissible show')
            # return redirect('dashboard:createleave')

        # messages.error(request,'failed to Request a Tournment,please check entry dates',extra_tags = 'alert alert-warning alert-dismissible show')
        # return redirect('dashboard:createleave')

    dataset = dict()
    form = LeaveCreationForm()
    form1 = PlayerCreationForm()
    form2 = HeatFormSet()


    dataset['form'] = form
    dataset['form1'] = form1
    dataset['form2'] = form2


    dataset['title'] = 'Tournment Details'
    return render(request,'dashboard/create_leave.html',dataset)
    # return HttpResponse('leave creation form')



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
    return render(request,'dashboard/leaves_recent.html',{'leave_list':leaves,'title':'leaves list - pending'})



def leaves_approved_list(request):
    if not (request.user.is_superuser and request.user.is_staff):
        return redirect('/')
    leaves = Leave.objects.all_approved_leaves() #approved leaves -> calling model manager method
    return render(request,'dashboard/leaves_approved.html',{'leave_list':leaves,'title':'approved leave list'})



def leaves_view(request,id):
    if not (request.user.is_authenticated):
        return redirect('/')

    leave = get_object_or_404(Leave, id = id)
    employee = Employee.objects.filter(user = leave.user)[0]
    print(employee)
    return render(request,'dashboard/leave_detail_view.html',{'leave':leave,'employee':employee,'title':'{0}-{1} leave'.format(leave.user.username,leave.status)})

from django import forms

def leaves_edit(request,id):
    players = None
    document = None
    HeatFormSet = modelformset_factory(Heats, fields=('tournment', 'rounds', 'player1', 'player2'), extra=1)
    leave = get_object_or_404(Leave, pk=id)
    if Players.objects.filter(tournment=leave).exists():
        players = get_object_or_404(Players, tournment=leave)
    if Document.objects.filter(tournament=leave).exists():
        document = Document.objects.filter(tournament=leave)
    # document = Document.objects.filter(tournament=leave).values()
    user = request.user
    if request.method == 'POST':
        #Heats.objects.get(tournment=Leave.objects.get(name=request.POST['fd_tournment']).id)
        form = LeaveCreationForm(data=request.POST, instance=leave)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.name = request.POST.get('name')
            print('===================')
            print(instance.name)
            print('===================')
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            BASE_DIR1 = os.path.dirname(BASE_DIR)
            BASE_DIR2 = os.path.dirname(BASE_DIR1)
            # Directory
            directory = str(user) + "--" + str(instance.name)

            # Parent Directory path
            url = os.path.join(BASE_DIR1, 'media')

            # Path
            path = os.path.join(url, directory)

            # Create the directory
            os.mkdir(path)
            print("Directory '% s' created" % directory)
            instance.rounds = request.POST.get('rounds')
            x = int(instance.rounds)
            # print('hdfahsgcvaskhcgashgcasihckashc',x)
            for i in range(1, x + 1):
                directory1 = "round-" + str(i)
                path1 = os.path.join(path, directory1)
                os.mkdir(path1)
                # print(directory1)

            instance.save()
            # print(instance.defaultdays)
            messages.success(request, 'Tournment first part is completed',
                             extra_tags='alert alert-success alert-dismissible show')
    if request.method == 'POST' and not form.is_valid():
        form1 = PlayerCreationForm(data=request.POST, prefix='form1')
        form = LeaveCreationForm(prefix='form')
        if form1.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            messages.success(request, 'Player created sucessfully',
                             extra_tags='alert alert-success alert-dismissible show')
    if request.method == 'POST' and not form.is_valid():
        HeatFormSet = modelformset_factory(Heats, fields=('tournment', 'rounds', 'player1', 'player2'), extra=0,
                                           max_num=0)
        user = request.user
        if request.method == 'GET':
            formset = HeatFormSet(queryset=Heats.objects.filter(user=user))
        elif request.method == 'POST':
            formset = HeatFormSet(request.POST, queryset=Heats.objects.filter(user=user))
            formset1 = DocumentFormSet(request.POST or None, form_kwargs={'id': id, 'instance': document})
            if formset.is_valid():
                for form in formset:
                    instance = form.save(commit=False)
                    instance.user = user
                    form.save()
                    print('empty form')
                    formset = HeatFormSet()
                return redirect('dashboard:createleave1')
            if formset1.is_valid():
                for form in formset1:
                    instance = form.save(commit=False)
                    instance.user = user
                    form.save()
                    print('empty form')
                    formset1 = DocumentForm()
                return redirect('dashboard:createleave1')
    dataset = dict()

    form = LeaveCreationForm(request.POST or None, instance = leave)
    if players is not None:
        form1 = PlayerCreationForm(request.POST or None, instance = players)
    else:
        form1 = PlayerCreationForm()
    formset = HeatFormSet(queryset=Heats.objects.filter(tournment=leave))
    # DocumentFormSet = formset_factory(DocumentForm, extra=1)
    DocumentFormSet = modelformset_factory(Document, fields=['tournament', 'rounds', 'games', 'loc',],
                                           widgets={
                                               'rounds': forms.Select(choices=[("Round-" + str(i), "Round-" + str(i)) for i in range(1, (int(Leave.objects.get(pk=id).rounds) + 1))]),
                                               'games': forms.Select(choices=[(str(heat.player1) + "_vs_" + str(heat.player2), str(heat.player1) + "_vs_" + str(heat.player2))
                                                for heat in Heats.objects.filter(tournment=id)])
                                            },)
    if document is not None:
        formset1 = DocumentFormSet(queryset=document)
        # formset1 = DocumentFormSet(request.POST or None, form_kwargs={'id': id})
        # formset1 = DocumentFormSet(initial=[{'document': doc} for doc in document], form_kwargs={'id': id})
        # print(formset1)
    else:
        formset1 = DocumentFormSet()
    # print(formset1)

    #print('>>>>>>>>>>>>>>>>>>')
    #form.name = 'ghhhjhj'
    #print(form)
    #print('>>>>>>>>>>>>>>>>>>')
    #print(id)
    #print('>>>>>>>>>>>>>>>>>>')
    dataset['form'] = form
    dataset['form1'] = form1
    dataset['formset'] = formset
    dataset['formset1'] = formset1
    # dataset['form4'] = form4

    dataset['title'] = 'Tournament Details'
    dataset['flag'] = 3
    return render(request, 'dashboard/create_player.html', dataset)


def approve_leave(request,id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leave = get_object_or_404(Leave, id = id)
    user = leave.user
    employee = Employee.objects.filter(user = user)[0]
    leave.approve_leave

    messages.error(request,'Tournment successfully approved for {0}'.format(employee.get_full_name),extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('dashboard:userleaveview', id = id)


def cancel_leaves_list(request):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leaves = Leave.objects.all_cancel_leaves()
    return render(request,'dashboard/leaves_cancel.html',{'leave_list_cancel':leaves,'title':'Cancel leave list'})



def unapprove_leave(request,id):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return redirect('/')
    leave = get_object_or_404(Leave, id = id)
    leave.unapprove_leave
    return redirect('dashboard:leaveslist') #redirect to unapproved list




def cancel_leave(request,id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leave = get_object_or_404(Leave, id = id)
    leave.leaves_cancel

    messages.success(request,'Tournment is canceled',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('dashboard:canceleaveslist')#work on redirecting to instance leave - detail view


# Current section -> here
def uncancel_leave(request,id):
    if not (request.user.is_superuser and request.user.is_authenticated):
        return redirect('/')
    leave = get_object_or_404(Leave, id = id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()
    messages.success(request,'Tournment is uncanceled,now in pending list',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('dashboard:canceleaveslist')#work on redirecting to instance leave - detail view



def leave_rejected_list(request):

    dataset = dict()
    leave = Leave.objects.all_rejected_leaves()

    dataset['leave_list_rejected'] = leave
    return render(request,'dashboard/rejected_leaves_list.html',dataset)



def reject_leave(request,id):
    dataset = dict()
    leave = get_object_or_404(Leave, id = id)
    leave.reject_leave
    messages.success(request,'Tournment is rejected',extra_tags = 'alert alert-success alert-dismissible show')
    return redirect('dashboard:leavesrejected')

    # return HttpResponse(id)


def unreject_leave(request,id):
    leave = get_object_or_404(Leave, id = id)
    leave.status = 'pending'
    leave.is_approved = False
    leave.save()
    messages.success(request,'Tournment is now in pending list ',extra_tags = 'alert alert-success alert-dismissible show')

    return redirect('dashboard:leavesrejected')



# Rabotec staffs leaves table user only
def view_my_leave_table(request):
    # work on the logics
    if request.user.is_authenticated:
        user = request.user
        leaves = Leave.objects.filter(user = user)
        employee = Employee.objects.filter(user = user).first()
        print(leaves)
        dataset = dict()
        dataset['leave_list'] = leaves
        dataset['employee'] = employee
        dataset['title'] = 'Leaves List'
    else:
        return redirect('accounts:login')
    return render(request,'dashboard/staff_leaves_table.html',dataset)

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
    return render(request,'dashboard/admin_tournment_table.html',dataset)






# Birthday
def birthday_this_month(request):	
    if not request.user.is_authenticated:
        return redirect('/')

    employees = Employee.objects.birthdays_current_month()
    month = datetime.date.today().strftime('%B')#am using this to get the month for template rendering- making it dynamic
    context = {
    'birthdays':employees,
    'month':month,
    'count_birthdays':employees.count(),
    'title':'Birthdays'
    }
    return render(request,'dashboard/birthdays_this_month.html',context)

def user_dashboard(request):
    #content = Content.objects.all()
    # user = request.user
    # 	leaves = Leave.objects.filter(user = user)

    # 	print(leaves)
    # 	dataset = dict()
    # 	dataset['leave_list'] = leaves
    # 	dataset['employee'] = employee
    # 	dataset['title'] = 'Leaves List'
    dataset = dict()
    user = request.user
    employee = Employee.objects.filter(user = user).first()
    # leave = get_object_or_404(Leave, id = id)
    # heat = heats.tournment
    # employee = Employee.objects


    # leaves = Leave.objects.all_approved_leaves()
    # heats = Heats.objects.filter(leave = leave)[0]


    leaves = Leave.objects.filter(user = user)
    # employee = Employee.objects.all()
    dataset['leave_list'] = leaves
    dataset['employee'] = employee
    return render(request, 'dashboard/user_dashboard.html',dataset)
    


# def dashboard_view1(request,id):
#     content = Content.objects.all()
#     dataset = dict()
#     user = heat.user
#     leave = get_object_or_404(Heats,id=id)
#     heat = heat.id
#     heats = Heats.objects.filter(tournment_id=heat)
#     # dataset['leave_list'] = leaves
#     dataset['heats'] = heats
#     dataset['content'] = content
#     return render(request, 'app/dashboard.html',dataset)


def dashboard_view_analysis(request,id):
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
    return render(request, 'app/dashboard1.html',dataset1)


def test(request):
    # content = Content.objects.all()
    # # item_json = serializers.serialize('xml', content)
    # tmpJson = serializers.serialize("json",content)
    # tmpObj = json.loads(tmpJson)

    # context = {
    #     "content": content,
    #     "tmpObj": tmpObj
    # }
    return render(request, 'app/test.html')


def test2(request,id):
    dataset = dict()
    doc_list = []
    tournament = None
    leave = get_object_or_404(Leave, id = id)
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
    return render(request, 'app/test2.html',dataset)


def dashboard_view1(request,id):
    dataset = dict()
    doc_list = []
    item = {}
    document = get_object_or_404(Document, pk=id)
    leave = get_object_or_404(Leave,id=int(document.tournament.id))
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
    dataset['content'] = [{'content': s}]
    dataset['document'] = doc_list
    return render(request, 'app/dashboard.html',dataset)	


def test4(request):
    return render(request, 'app/test4.html')

def broadcast(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        #handle_uploaded_file(request.FILES['docfile'], str(request.FILES['docfile']))
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            options =[]
            with open('media/documents/game-1.pgn', 'r') as reader:
                # for line in reader:
                #     currentPlace = line[:-1]
                #     options.append(currentPlace)
                #     print(options)
                s=reader.read()
                myobject = Content(content=s)
                myobject.save()
            

            # Redirect to the document list after POST
            return redirect('dashboard:broadcast')
            # return HttpResponseRedirect(reverse('users:list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    content = Content.objects.all()
    # Render list page with the documents and the form
    return render(request,'app/list.html',{'documents': documents,'content':content, 'form': form})

from pathlib import Path
import shutil
from cron import cron_job

def uploadpgn(request):
    if not request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    print("create uploadpgn view here")
    if request.method == 'POST':
        print(request.POST)
        # TODO total no of form is not changing when a new form is added
        for i in range(int(20)):
            if "form-" + str(i) + "-id" in request.POST:
                if request.POST["form-" + str(i) + "-id"] != "":
                    id = request.POST["form-" + str(i) + "-id"]
                    document = Document.objects.get(pk=id)
                else:
                    document = Document()
                if request.POST["form-" + str(i) + "-loc"] == "":
                    messages.error(request, 'Please Enter PGN File Location',
                                   extra_tags='alert alert-danger alert-dismissible show')
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    if os.path.isfile(request.POST["form-" + str(i) + "-loc"]):
                        pass
                    else:
                        messages.error(request, 'PGN File Location you entered is not a valid file location',
                                       extra_tags='alert alert-danger alert-dismissible show')
                        return redirect(request.META.get('HTTP_REFERER'))
                if request.POST["form-" + str(i) + "-tournament"] != "":
                    document.tournament = Leave.objects.get(pk=request.POST["form-" + str(i) + "-tournament"])
                    document.rounds = request.POST["form-" + str(i) + "-rounds"]
                    document.games = request.POST["form-" + str(i) + "-games"]
                    document.loc = request.POST["form-" + str(i) + "-loc"]
                    document.save()
                    file_name = request.user.username + "_" + request.POST["form-" + str(i) + "-games"]
                    loc = os.path.join(settings.BASE_DIR, 'media', request.user.username
                                            + "--" + Leave.objects.get(pk=request.POST["form-" + str(i)
                                            + "-tournament"]).name, request.POST["form-" + str(i) + "-rounds"],
                                            request.POST["form-" + str(i) + "-games"])
                    Path(loc).mkdir(parents=True, exist_ok=True)
                    fileitem = request.POST["form-" + str(i) + "-loc"]
                    file_loc = os.path.join(settings.BASE_DIR, 'media', request.user.username
                                            + "--" + Leave.objects.get(pk=request.POST["form-" + str(i)
                                            + "-tournament"]).name, request.POST["form-" + str(i) + "-rounds"],
                                            request.POST["form-" + str(i) + "-games"], file_name + ".pgn")
                    print(file_loc)
                    with open(fileitem) as source:
                        with open(file_loc, "w") as destination:
                            for line in source:
                                destination.write(line)
                    cron_job.start(loc, file_name, fileitem)
        messages.success(request, 'Pgn upload successfully', extra_tags='alert alert-success alert-dismissible show')
        return redirect(request.META.get('HTTP_REFERER'))

from django.shortcuts import render
from django.contrib.auth import login, authenticate
from users.forms import SignUpForm,DetailForm
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
    if not request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    print("create player view here")
    if request.method == 'POST':
        form = PlayerCreationForm(data = request.POST)
        print(form)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            instance = form.save(commit = False)
            # user.refresh_from_db()
            user = request.user
            instance.user = user
            instance.save()
            messages.success(request,'Player created sucessfully',extra_tags = 'alert alert-success alert-dismissible show')
            messages.success(request,'You can add more players by going to the create player section again!!!!',extra_tags = 'alert alert-success alert-dismissible show')
            return redirect('dashboard:createleave')
        formset_view(request)
        messages.success(request,'You can add more players by going to the create player section again!!!!',extra_tags = 'alert alert-success alert-dismissible show')
        # return redirect('dashboard:createleave')
    dataset = dict()
    form = PlayerCreationForm()
    dataset['form'] = form
    dataset['title1'] = 'Create Players'
    return render(request,'dashboard/create_leave.html',dataset)


def heats(request,id):
    print("create opponents view here")
    if not request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    ls = Leave.objects.get(id=id)

    if ls in request.user.user.all():
        
        if request.method == 'POST':
            form = HeatsCreationForm(data = request.POST)
            if form.is_valid():
                instance = form.save(commit = False)
                user = request.user
                instance.user = user
                instance.save()
                
                messages.success(request,'Opponents created sucessfully',extra_tags = 'alert alert-success alert-dismissible show')




                # user.refresh_from_db()


                # instance.tournment = Leave.objects.filter(user=instance.user )

                #
                # return redirect('dashboard:createleave')
            # messages.error(request,'failed to create opponents,please check entry dates',extra_tags = 'alert alert-warning alert-dismissible show')
            # return redirect('dashboard:createleave')
    dataset = dict()
    form = HeatsCreationForm()
    dataset['form'] = form
    dataset['title'] = 'Create Rounds'
    return render(request,'dashboard/create_leave.html',dataset)




from django.forms import modelformset_factory,formset_factory
def formset_view(request): 
    print("create opponents2 view here")
    context ={} 
  
    # creating a formset and 5 instances of GeeksForm 
    HeatFormSet = modelformset_factory(Heats,fields=('tournment','rounds','player1','player2'),extra=0,max_num=1) 
    if request.method=='POST':
        form = HeatFormSet(data=request.POST,queryset=Heats.objects.none())
        if form.is_valid():
    
            print('valid form')

            for form in form:

                if form.is_valid():

                    print('in for loop after valid form1')

                    instance = form.save(commit=False)
                    user = request.user
                    instance.user = user
                    tournment = Leave.objects.filter(user=user )
                    # instance.tournment = request.POST.get('tournment')
                    # instance.rounds = request.POST.get('rounds')
                    # instance.player1 = request.POST.get('player1')
                    # instance.player2 = request.POST.get('player2')
                    # instance.tournment = form.cleaned_data['tournment']
                    # instance.rounds = form.cleaned_data['rounds']
                    # instance.player1 = form.cleaned_data['player1']
                    # instance.player2 = form.cleaned_data['player2']
                    instance.save()
                    messages.success(request,'Opponents created sucessfully',extra_tags = 'alert alert-success alert-dismissible show')

    form = HeatFormSet()  
    # print formset data if it is valid 
    if form.is_valid(): 
        for form in form: 
            print(form.cleaned_data)

    # Add the formset to context dictionary 
    context['form']= form
    context['flag']= 2
    return render(request, "dashboard/create_player.html", context)



# def formset_view(request): 
#     context ={} 
  
#     # creating a formset and 5 instances of GeeksForm 
#     GeeksFormSet = formset_factory(HeatsCreationForm, extra = 3) 
#     formset = GeeksFormSet(request.POST or None) 
      
#     # print formset data if it is valid 
#     if formset.is_valid(): 
#         for form in formset: 
#             print(form.cleaned_data) 
              
#     # Add the formset to context dictionary 
#     context['formset']= formset 
#     return render(request, "dashboard/create_player.html", context) 
# def formset_view1(request,id):
#     template_name = 'dashboard/create_leave.html'
#     heading_message = 'Model Formset Demo'
#     HeatFormSet = modelformset_factory(Heats,fields=('tournment','rounds','player1','player2'),extra=0,max_num=1)
    
#     ls = Leave.objects.get(id=id)

#     if ls in request.user.user.all():
#         if request.method == 'GET':
#             formset = HeatFormSet(queryset=Heats.objects.none())
#         elif request.method == 'POST': 
#             formset = HeatFormSet(request.POST)  
#             if formset.is_valid(): 
#                 for form in formset:
#                     instance = form.save(commit=False)
#                     user = request.user
#                     instance.user = user
#                     form.save()
#                 # return redirect('dashboard:book1')

#     return render(request, template_name, {
#         'formset': formset,
#         'heading': heading_message,
#     })
    
    
    
    
def leave_creation1(request):
    HeatFormSet = modelformset_factory(Heats,fields=('tournment','rounds','player1','player2') ,extra=1)
    if request.method == 'POST':
        form = LeaveCreationForm(data = request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            user = request.user
            instance.user = user
            instance.name=request.POST.get('name')
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            BASE_DIR1 = os.path.dirname(BASE_DIR)
            BASE_DIR2 =os.path.dirname(BASE_DIR1)
            # Directory
            directory = str(user ) + "--" + str(instance.name)

            # Parent Directory path
            url= os.path.join(BASE_DIR1, 'media')

            # Path
            path = os.path.join(url, directory)

            # Create the directory

            os.mkdir(path)
            print("Directory '% s' created" % directory)
            instance.rounds=request.POST.get('rounds')
            x=int(instance.rounds)
            # print('hdfahsgcvaskhcgashgcasihckashc',x)
            for i in range(1,x+1) :
                directory1 = "round-"+ str(i)

                path1 = os.path.join(path, directory1)
                os.mkdir(path1)
                # print(directory1)

            instance.save()

            # print(instance.defaultdays)
            messages.success(request,'Tournment first part is completed',extra_tags = 'alert alert-success alert-dismissible show')
            # return redirect('dashboard:createleave')

        # messages.error(request,'failed to Request a Tournment,please check entry dates',extra_tags = 'alert alert-warning alert-dismissible show')
        # return redirect('dashboard:createleave')

    if request.method == 'POST' and not form.is_valid():
        form1 = PlayerCreationForm(data = request.POST,prefix='form1')

        form = LeaveCreationForm(prefix='form')
        if form1.is_valid():
            instance = form.save(commit = False)
            user = request.user
            instance.user = user
            instance.save()
            messages.success(request,'Player created sucessfully',extra_tags = 'alert alert-success alert-dismissible show')

    # if request.method == 'POST' and not form.is_valid():
    # 	broadcast(request)

    # 	form4 = DocumentForm(request.POST, request.FILES,prefix='form4')

    # 	form = LeaveCreationForm(prefix='form')
    # 	if form4.is_valid():
    # 		newdoc = Document(docfile = request.FILES['docfile'])
    # 		newdoc.save()
    # 		options =[]
    # 		with open('media/documents/game-1.pgn', 'r') as reader:
    # 			s=reader.read()
    # 			myobject = Content(content=s)
    # 			myobject.save()
    # 		messages.success(request,'PGN uploaded sucessfully',extra_tags = 'alert alert-success alert-dismissible show')
    # 		return redirect('dashboard:createleave1')
        #handle_uploaded_file(request.FILES['docfile'], str(request.FILES['docfile']))

        # if request.method == 'POST' and not form.is_valid():
    # 	PlayerFormSet = modelformset_factory(Players,fields=('name','last','gender','rating','title','ranking'))
    # 	if request.method == 'GET':
    # 		formset1 = PlayerFormSet(queryset=Players.objects.none())
    # 	elif request.method == 'POST':
    # 		formset1 = PlayerFormSet(request.POST)
    # 		if formset1.is_valid():
    # 			for form in formset1:
    # 				instance = form.save(commit=False)
    # 				user = request.user
    # 				instance.user = user
    # 				form.save()
    #  	messages.success(request,'Player created sucessfully',extra_tags = 'alert alert-success alert-dismissible show')

    if request.method == 'POST' and not form.is_valid():
        HeatFormSet = modelformset_factory(Heats,fields=('tournment','rounds','player1','player2'),extra=0, max_num=0)
        user = request.user
        if request.method == 'GET':
            formset = HeatFormSet(queryset=Heats.objects.filter(user=user))
        elif request.method == 'POST':
            formset = HeatFormSet(request.POST,queryset=Heats.objects.filter(user=user))
            if formset.is_valid():
                for form in formset:
                    instance = form.save(commit=False)
                    user = request.user
                    instance.user = user
                    # instance.tournment = Leave.objects.filter(user = user)
                    form.save()
                    print('empty form')
                    formset = HeatFormSet()
                return redirect('dashboard:createleave1')

    # else:
    # 	form2 = HeatFormSet(prefix='form1')
    dataset = dict()
    form = LeaveCreationForm()
    form1 = PlayerCreationForm()
    formset = HeatFormSet()
    # form4 = DocumentForm()

    dataset['form'] = form
    dataset['form1'] = form1
    dataset['formset'] = formset
    # dataset['form4'] = form4

    dataset['title'] = 'Tournment Details'
    dataset['flag'] = 1
    return render(request,'dashboard/create_player.html',dataset)
    # return HttpResponse('leave creation form')

