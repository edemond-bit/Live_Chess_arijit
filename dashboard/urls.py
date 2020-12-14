from django.urls import path
from .import views


app_name = 'dashboard'

urlpatterns = [
    path('welcome/',views.dashboard,name='dashboard'),

    # Employee
    path('employee/all/',views.dashboard_employees,name='employees'),
    path('employee/create/',views.dashboard_employees_create,name='employeecreate'),
    path('employee/profile/<int:id>/',views.dashboard_employee_info,name='employeeinfo'),
    path('employee/profile/edit/<int:id>/',views.employee_edit_data,name='edit'),
    path('user/create/',views.dashboard_user_create,name='usercreate'),

    # Emergency
    path('emergency/create/',views.dashboard_emergency_create,name='emergencycreate'),
    path('emergency/update/<int:id>',views.dashboard_emergency_update,name='emergencyupdate'),

    # Family
    path('family/create/',views.dashboard_family_create,name='familycreate'),
    path('family/edit/<int:id>',views.dashboard_family_edit,name='familyedit'),
    
    #Bank
    path('bank/create/',views.dashboard_bank_create,name='bankaccountcreate'),

    #---work-on-edit-view------#
    path('tournment/apply/',views.leave_creation1,name='createleave1'),
    path('tournment/apply/',views.leave_creation,name='createleave'),
    path('tournment/pending/all/',views.leaves_list,name='leaveslist'),
    path('tournment/approved/all/',views.leaves_approved_list,name='approvedleaveslist'),
    path('tournment/cancel/all/',views.cancel_leaves_list,name='canceleaveslist'),
    path('tournment/all/view/<int:id>/',views.leaves_view,name='userleaveview'),
    path('tournment/all/edit/<int:id>/',views.leaves_edit,name='userleaveedit'),
    path('tournment/view/table/',views.view_my_leave_table,name='staffleavetable'),
    path('tournment/approve/<int:id>/',views.approve_leave,name='userleaveapprove'),
    path('tournment/unapprove/<int:id>/',views.unapprove_leave,name='userleaveunapprove'),
    path('tournment/cancel/<int:id>/',views.cancel_leave,name='userleavecancel'),
    path('tournment/uncancel/<int:id>/',views.uncancel_leave,name='userleaveuncancel'),
    path('tournment/rejected/all/',views.leave_rejected_list,name='leavesrejected'),
    path('tournment/reject/<int:id>/',views.reject_leave,name='reject'),
    path('tournment/unreject/<int:id>/',views.unreject_leave,name='unreject'),
    path('tournment/admin/view/table/',views.admin_tournment_table,name='adminleavetable'),
    
    # BIRTHDAY ROUTE
    # path('birthdays/all/',views.create_book_normal,name='birthdays'),
    path('book/',views.formset_view,name='book'),
    # path('book1/<int:id>',views.formset_view1,name='book1'),
    path('user/dashboard/', views.user_dashboard, name='dashboard1'),
    path('broadcast/game/<int:id>/', views.dashboard_view1, name='dashboard11'),
    path('broadcast/analysis/<int:id>/', views.dashboard_view_analysis, name='dashboard_view_analysis'),
    path('test/', views.test, name='test'),
    path('test2/<int:id>/', views.test2, name='test2'),
    path('test4/',views. test4, name='test4'),
    
    # path('', views.signup, name='profile-signup'),
    path('create-user/',views.signup_view,name='register'),

    #-----player----#
    path('player/create/',views.player_creation,name='createplayer'),
    path('heats/create/<int:id>',views.heats,name='heats'),
    path('broadcast/create/',views.broadcast,name='broadcast'),

    #----upload pgn----#
    path('uploadpgn/',views.uploadpgn,name='uploadpgn'),
]
