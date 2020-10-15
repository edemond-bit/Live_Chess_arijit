from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




# class UserAddForm(UserCreationForm):
# 	firstname = forms.CharField(
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
# 	lastname = forms.CharField(
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
# 	email = forms.EmailField(
# 		label='',
# 		max_length=254,
# 		widget=forms.EmailInput(
# 			attrs={
# 				"placeholder": "Email",
# 				"class": "form-control"
# 			}
# 		)
# 	)

# 	username = forms.CharField(
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

# 	password1 = forms.CharField(
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

# 	password2 = forms.CharField(
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
	
# 	class Meta:
# 		model = User
# 		fields = ('firstname','lastname','username', 'email', 'password1', 'password2')

# class SignUpForm(UserCreationForm):
#     first_name = forms.CharField(max_length=100, help_text='Last Name')
#     last_name = forms.CharField(max_length=100, help_text='Last Name')
#     email = forms.EmailField(max_length=150, help_text='Email')


#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
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




class UserLogin(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))


