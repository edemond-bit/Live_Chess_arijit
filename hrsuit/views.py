from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect

from tournment.models import Leave
from users.models import *
from tournment.forms import LeaveCreationForm
# from leave.forms import CommentForm
from django.contrib.auth.models import User



def index_view(request):
    dataset = dict()
    user = request.user
	
    leaves = Leave.objects.all_approved_leaves()
    employee = Employee.objects.all()
    dataset['leave_list'] = leaves
    dataset['employee'] = employee
	
	
	
	
	
    return render(request,'_layout.html',dataset)
	