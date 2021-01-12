from django.db import models
from .manager import LeaveManager,HeatManager, DocumentManager
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from timezone_field import TimeZoneField
import pytz
# Create your models here.
Standard_Chess_Position = 'Standard Chess Position'
Chess960 = 'Chess960'
King_Of_The_Hill = 'King Of The Hill'


LEAVE_TYPE = (
(Standard_Chess_Position , 'Standard Chess Position'),
(Chess960 , 'Chess960'),
(King_Of_The_Hill , 'King Of The Hill'),

)


DAYS = 10


class Leave(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name="user")
	name = models.CharField(verbose_name=_('Tournment Name'),max_length=50,null=True,blank=False)
	desc = models.CharField(verbose_name=_('Tournment Description'),max_length=250,null=True,blank=False)
	location = models.CharField(verbose_name=_('Location'),max_length=50,null=True,blank=False)
 	
	country = models.CharField(verbose_name=_('Country'),max_length=50,null=True,blank=False)
 	
	laws = models.CharField(verbose_name=_('Laws Of Chess'),max_length=50,null=True,blank=False)
 	
  	
	type = models.CharField(choices=LEAVE_TYPE,max_length=25,default=Standard_Chess_Position,null=True)
	startdate = models.DateField(verbose_name=_('Start Date'),null=True,blank=False)
	starttime = models.TimeField(verbose_name=_('Start Time'),help_text='Tournment start time is on ..',null=True,blank=True)
	enddate = models.DateField(verbose_name=_('End Date'),null=True,blank=False)
	endtime = models.TimeField(verbose_name=_('End Time'),help_text='Tournment end time is on ..',null=True,blank=True)
	timezone = TimeZoneField(default='Europe/London')
	rounds = models.PositiveIntegerField(_('Number of Rounds'),null=True,blank=False,default=0)
	status = models.CharField(max_length=12,default='pending') #pending,approved,rejected,cancelled
	is_approved = models.BooleanField(default=False) #hide
 
 
 
	
 
	
	
	created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
	updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)
    
	objects = LeaveManager()


	


	class Meta:
		verbose_name = _('Tournment')
		verbose_name_plural = _('Tournments')
		ordering = ['-created'] #recent objects



	def __str__(self):
		return ('{0}'.format(self.name))


	# @property
	# def is_live(self):
 #    if self.starttime is None or self.endtime is None :
 #        return False
 #    return (self.starttime <= timezone.now()) and (self.endtime >= timezone.now())	


	@property
	def pretty_leave(self):
		'''
		i don't like the __str__ of leave object - this is a pretty one :-)
		'''
		leave = self.type
		user = self.user
		# employee = user.employee_set.first().get_full_name
		return ('{0} - {1}'.format(user,leave))

	# @property
	# def days_left(self):
	# 	data = self.defaultdays
	# 	days_left = data - self.leave_days
	# 	self.defaultdays = days_left
	# 	return (self.defaultdays)	



	@property
	def leave_days(self):
		days_count = ''
		startdate = self.startdate
		enddate = self.enddate
		if startdate > enddate:
			return
		dates = (enddate - startdate)
		return dates.days



	@property
	def leave_approved(self):
		return self.is_approved == True




	@property
	def approve_leave(self):
		if not self.is_approved:
			self.is_approved = True
			self.status = 'approved'
			self.save()




	@property
	def unapprove_leave(self):
		if self.is_approved:
			self.is_approved = False
			self.status = 'pending'
			self.save()



	@property
	def leaves_cancelled(self):
		if self.is_approved or not self.is_approved:
			self.is_approved = False
			self.status = 'cancelled'
			self.save()



	# def uncancel_leave(self):
	# 	if  self.is_approved or not self.is_approved:
	# 		self.is_approved = False
	# 		self.status = 'pending'
	# 		self.save()

	# @property 
	# def half_day_leave(self):
	# 	halfdaydate=self.halfdaydate
	# 	today_date = datetime.date.today()
	# 	if halfdaydate >= today_date:
	# 		return halfdaydate
	# 	else:
	# 		return('You are choosing wrong dates')

	@property
	def reject_leave(self):
		if self.is_approved or not self.is_approved:
			self.is_approved = False
			self.status = 'rejected'
			self.save()



	@property
	def is_rejected(self):
		return self.status == 'rejected'



	
	# def save(self,*args,**kwargs):
	# 	data = self.defaultdays
	# 	days_left = data - self.leave_days
	# 	self.defaultdays = days_left
	# 	super().save(*args,**kwargs)
# class Rounds(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
#     tournment= models.ForeignKey(Leave,on_delete=models.CASCADE,null=True,blank=False)
# 	rounds = models.PositiveIntegerField(_('Select Players per Rounds'),null=True,blank=False,default=0)
# 	class Meta:
#         verbose_name = _('Round')
#         verbose_name_plural = _('Rounds')
#         ordering = ['rounds','created']
    
#     def __str__(self):
#         return self.user + self.tournment
    
class Players(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    NOT_KNOWN = 'Not Known'

    GENDER = (
    (MALE,'Male'),
    (FEMALE,'Female'),
    (OTHER,'Other'),
    (NOT_KNOWN,'Not Known'),
    )
    


    Women_GM = 'Women GM'
    International_Master = 'International Master'
    WOMEN_IM = 'WOMEN IM'
    FIDE_M = 'FIDE M'
    Women_FIDE_M = 'Women FIDE M'
    CM = 'CM'
    Women_CM = 'Women CM'
    National_Master = 'National Master'
    W_N_M= 'W N M'
    

    PLAYERTYPE = (
    (Women_GM,'Women GM'),
    (International_Master , 'International Master'),
    (WOMEN_IM , 'WOMEN_IM'),
    (FIDE_M , 'FIDE_M'),
    (Women_FIDE_M , 'Women_FIDE_M'),
    (CM , 'CM'),
    (Women_CM , 'Women_CM'),
    (National_Master , 'National_Master'),
    (W_N_M , 'W_N_M'),
    )
    
    '''
     Department Employee belongs to. eg. Transport, Engineering.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=125,blank=False)
    last = models.CharField(max_length=125,blank=False)
    gender = models.CharField(_('Gender'),max_length=9,default=MALE,choices=GENDER,blank=False)
    rating = models.PositiveIntegerField(_('FIDE Rating'),null=True,blank=True,default=0)
    COUNTRY_RATING= models.PositiveIntegerField(_('COUNTRY RATING'),null=True,blank=True,default=0)
    title = models.CharField(_('Title'),max_length=20,default=Women_GM,choices=PLAYERTYPE,blank=False)
    tournment = models.ForeignKey(Leave, on_delete=models.CASCADE, null=True)
	
    ranking = models.PositiveIntegerField(_('FIDE Ranking'),null=True,blank=True,default=0)
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)

    

    
    
    class Meta:
        verbose_name = _('Player')
        verbose_name_plural = _('Players')
        ordering = ['name','created']
    
    def __str__(self):
        return self.name + self.title
  
  
  
# class Players2(models.Model):
#     MALE = 'male'
#     FEMALE = 'female'
#     OTHER = 'other'
#     NOT_KNOWN = 'Not Known'

#     GENDER = (
#     (MALE,'Male'),
#     (FEMALE,'Female'),
#     (OTHER,'Other'),
#     (NOT_KNOWN,'Not Known'),
#     )
    
#     GM = 'GM'
#     MASTER = 'MASTER'
#     ROOKIE = 'ROOKIE'
#     WM = 'WM'

#     PLAYERTYPE = (
#     (GM,'GM'),
#     (MASTER , 'MASTER'),
#     (ROOKIE , 'ROOKIE'),
#     (WM , 'WM'),
#     )
    
#     '''
#      Department Employee belongs to. eg. Transport, Engineering.
#     '''
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=125,blank=False)
#     last = models.CharField(max_length=125,blank=False)
#     gender = models.CharField(_('Gender'),max_length=8,default=MALE,choices=GENDER,blank=False)
#     rating = models.PositiveIntegerField(_('FIDE Rating'),null=True,blank=True,default=0)
#     title = models.CharField(_('Gender'),max_length=8,default=GM,choices=PLAYERTYPE,blank=False)
	
#     ranking = models.PositiveIntegerField(_('FIDE Ranking'),null=True,blank=True,default=0)
#     created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    
#     updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)

    

    
    
#     class Meta:
#         verbose_name = _('Player2')
#         verbose_name_plural = _('Player2')
#         ordering = ['name','created']
    
#     def __str__(self):
#         return self.name + self.title


class Heats(models.Model):
	tournment= models.ForeignKey(Leave,on_delete=models.CASCADE,null=True,blank=False)
	rounds = models.PositiveIntegerField(_('Select Players per Rounds'),null=True,blank=False,default=0)
	player1 = models.ForeignKey(Players, related_name=_('player1'),on_delete=models.CASCADE,null=True,blank=False,max_length=125)
	player2 = models.ForeignKey(Players, related_name=_('player2'),on_delete=models.CASCADE,null=True,blank=False,max_length=125)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
	updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)
	objects = HeatManager()
    
    
	class Meta:
     
		verbose_name = _('Heat')
		verbose_name_plural = _('Heats')
		ordering = ['tournment','created']
		
	def __str__(self):
            return self.tournment.__str__() + ",  Rounds - " + self.rounds.__str__() + ",  Heat id -" +self.id.__str__()
    
    # @property
	# def approve_heat(self):
		
	# 	self.is_approved = True
	# 	self.status = 'approved'
	# 	self.save()    

class Document(models.Model):
	tournament = models.ForeignKey(Leave,on_delete=models.CASCADE,null=True)
	rounds = models.CharField(max_length=125, unique=True, null=True, blank=True)
	games = models.CharField(max_length=125, null=True, blank=True)
	loc = models.CharField(max_length=300, verbose_name="PGN File Location", null=True, blank=True)
	docfile = models.FileField(_('PGN'),upload_to='profiles',null=True,help_text='upload image size less than 2.0MB')
	objects = DocumentManager()

	def __str__(self):
		return self.tournament.__str__() + ",  Rounds - " + self.rounds.__str__() + ",  games - " +self.id.__str__()

class Content(models.Model):
	content = models.TextField()

	def __int__(self):
		return self.id
    
       
        
