from django import forms
from .models import Leave,Players,Heats,Document
from timezone_field import TimeZoneFormField
import datetime
from django.forms import formset_factory, modelformset_factory
from django.utils.translation import gettext_lazy as _


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


class PlayerCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=125, required=True, widget=forms.TextInput(attrs={'required': "required"}))

    class Meta:
        model = Players
        fields = ['name', 'last', 'gender', 'rating', 'title', 'ranking', 'COUNTRY_RATING']
        exclude = ['updated', 'created']
        error_messages = {
            'name': {
                'required': _("Please enter Player's name."),
            },
        }

    def clean_renewal_date(self):
        super().clean()


class HeatsCreationForm(forms.ModelForm):
    rounds = forms.IntegerField(required=True, label="Select Players per Rounds", widget=forms.NumberInput(attrs={'required': "required"}))
    player1 = forms.ModelMultipleChoiceField(queryset=Players.objects.all(), widget=forms.Select(attrs={'required': "required"}))
    player2 = forms.ModelMultipleChoiceField(queryset=Players.objects.all(), widget=forms.Select(attrs={'required': "required"}))

    class Meta:
        model = Heats
        fields = ['rounds', 'player1', 'player2']
        exclude = ['updated', 'created']


class DocumentForm(forms.ModelForm):
    docfile = forms.FileField(required=True, widget=forms.FileInput(attrs={'required': "required"}))

    class Meta:
        model = Document
        fields = ['rounds', 'games', 'docfile']
        error_messages = {
            'rounds': {
                'unique': _("This round has already been registered."),
            },
        }

    def clean_rounds(self):
        rounds = self.cleaned_data['rounds']
        if Document.objects.filter(rounds=rounds).exists():
            raise ValidationError("Round already exists")
        return rounds