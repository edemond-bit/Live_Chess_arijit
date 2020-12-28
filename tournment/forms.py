from django import forms
from .models import Leave,Players,Heats,Document

# from .models import Comment
from timezone_field import TimeZoneFormField
import datetime
from django.forms import formset_factory, modelformset_factory

class LeaveCreationForm(forms.ModelForm):
    timezone = TimeZoneFormField()
    class Meta:
        model = Leave
        fields = ['name','desc','location','type','country','laws','startdate','starttime','enddate','endtime','timezone','rounds']
        exclude = ['user','hrcomments','status','is_approved','updated','created']
    def clean_enddate(self):
        enddate = self.cleaned_data['enddate']
        startdate = self.cleaned_data['startdate']
        today_date = datetime.date.today()	
        return enddate

		
		
		
	
    	
		
			
		
		



	

		# if (startdate or enddate) < today_date:# both dates must not be in the past
		# 	raise forms.ValidationError("Selected dates are incorrect,please select again")

		# elif startdate >= enddate:# TRUE -> FUTURE DATE > PAST DATE,FALSE other wise
		# 	raise forms.ValidationError("Selected dates are wrong")

		

class PlayerCreationForm(forms.ModelForm):
    
	class Meta:
		model = Players

		fields = ['tournment','name','last','gender','rating','title','ranking','COUNTRY_RATING',]
		
		exclude = ['updated','created']
	def clean_renewal_date(self):
		super().clean()
     
  
	
        
        
        # Check if a date is not in the past. 
        

        # Remember to always return the cleaned data.
        


class HeatsCreationForm(forms.ModelForm):
    
	class Meta:
		model = Heats
		
		fields = ['tournment','rounds','player1','player2']
		
		exclude = ['updated','created']
  
  
	# def __init__(self, user, *args, **kwargs):
	# 	super(HeatsCreationForm, self).__init__(*args, **kwargs)
	# 	self.fields['tournment'].queryset = Leave.objects.filter(user=user)
# HeatsCreationset = formset_factory(HeatsCreationForm, extra=1)		
        
        
  
# from django.forms import formset_factory


# HeatFormset = formset_factory(HeatsCreationForm, extra=1) 

  
# class CommentForm(forms.ModelForm):

# 	class Meta:
# 		model = Comment
# 		exclude = ['updated','created','leave']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['tournament', 'rounds', 'games', 'loc',]