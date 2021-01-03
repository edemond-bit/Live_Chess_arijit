from django import forms
from users.models import Role,Department,Nationality,Religion,Bank,Emergency,Relationship,Employee,Details
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# # EMPLoYEE
# class EmployeeCreateForm(forms.ModelForm):
# 	employeeid = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'please enter 5 characters without RGL or slashes eg. A0025'}))
# 	image = forms.ImageField(widget=forms.FileInput(attrs={'onchange':'previewImage(this);'}))
# 	class Meta:
# 		model = Employee
# 		exclude = ['is_blocked','is_deleted','created','updated']
# 		widgets = {
# 				'bio':forms.Textarea(attrs={'cols':5,'rows':5})
# 		}


# 	# def clean_user(self):
# 	# 	user = self.cleaned_data['user'] #returns <User object>,not id as in [views <-> templates]

# 	# 	qry = Employee.objects.filter(user = user)#check, whether any employee exist with username - avoid duplicate users - > many employees
# 	# 	if qry:
# 	# 		raise forms.ValidationError('Employee exists with username already')
# 	# 	return user





# class EmergencyCreateForm(forms.ModelForm):

# 	class Meta:
# 		model = Emergency
# 		fields = ['employee','fullname','tel','location','relationship']





# # FAMILY

# class FamilyCreateForm(forms.ModelForm):

# 	class Meta:
# 		model = Relationship
# 		fields = ['employee','status','spouse','occupation','tel','children','nextofkin','contact','relationship','father','foccupation','mother','moccupation']



# class BankAccountCreation(forms.ModelForm):

# 	class Meta:
# 		model = Bank
# 		fields = ['employee','name','branch','account','salary']

# class UserAddForm(UserCreationForm):
#     firstname = forms.CharField(
# 		label='',
# 		max_length=30,
# 		min_length=5,
# 		required=True,
# 		widget=forms.TextInput(
# 			attrs={
# 				"placeholder": "Firstname",
# 				"class": "form-control"
# 			}
# 		)
# 	)
#     lastname = forms.CharField(
    
    	
	
	
# 		label='',
# 		max_length=30,
# 		min_length=5,
# 		required=True,
# 		widget=forms.TextInput(
# 			attrs={
# 				"placeholder": "Lastname",
# 				"class": "form-control"
# 			}
# 		)
# 	)
#     username = forms.CharField(
	
# 		label='',
# 		max_length=30,
# 		min_length=5,
# 		required=True,
# 		widget=forms.TextInput(
# 			attrs={
# 				"placeholder": "Username",
# 				"class": "form-control"
# 			}
# 		)
# 	)
#     email = forms.EmailField(

	
# 		label='',
# 		max_length=255,
# 		required=True,
# 		widget=forms.EmailInput(
# 			attrs={
# 				"placeholder": "Email",
# 				"class": "form-control"
# 			}
# 		)
# 	)
    
#     password1 = forms.CharField(

	
# 		label='',
# 		max_length=30,
# 		min_length=8,
# 		required=True,
# 		widget=forms.PasswordInput(
# 			attrs={
# 				"placeholder": "Password",
# 				"class": "form-control"
# 			}
# 		)
# 	)
#     password2 = forms.CharField(

	
# 		label='',
# 		max_length=30,
# 		min_length=8,
# 		required=True,
# 		widget=forms.PasswordInput(
# 			attrs={
# 				"placeholder": "Confirm Password",
# 				"class": "form-control"
# 			}
# 		)
# 	)
#     class Meta:
#         model = User
#         fields = ('firstname','lastname','username', 'email', 'password1', 'password2')

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='')
    last_name = forms.CharField(max_length=100, help_text='')
    email = forms.EmailField(max_length=150, help_text='')


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email', 'password1', 'password2',)	
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class DetailForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'onchange':'previewImage(this);'}))

    class Meta:
        model = Details
        fields = ('age', 'bio', 'gender', 'contact', 'dob', 'image',)
        widgets = {'dob': DateInput()}
