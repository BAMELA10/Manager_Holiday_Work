from .models import *
from django import forms
from Account.models import *
import datetime as dt

class Holiday_form(forms.ModelForm):
    code = forms.CharField(max_length=100,disabled=True,required=False,
                               widget=forms.TextInput({
                                   'class': 'form-control col-md-6 rounded-0 fs-4',
                                   'placeholder': 'Code'}))
    start_date = forms.DateField(required=True, widget=forms.DateInput({
                                   'class': 'form-control col-md-6 rounded-0 fs-4',
                                   'placeholder': 'Date',
                                   'type': 'Date'
                                   }))
    end_date = forms.DateField(required=True, widget=forms.DateInput({
                                   'class': 'form-control col-md-6 rounded-0 fs-4',
                                   'placeholder': 'Date',
                                   'type': 'Date'
                                   }))
    beneficiary = forms.ModelChoiceField(required=True, widget=forms.Select({
                                   'class': 'form-control col-md-6 rounded-0',
                                   'placeholder': 'Employe'}),
                                    queryset=User.objects.all())
    
    class Meta:
        model = Holiday
        fields = ['code', 'start_date', 'end_date', 'beneficiary']
    
    def clean(self):
        #verification de l'ordre entre la date de debut et la date de fin (date debut < date de fin)
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        
        if start_date :
            if start_date <= dt.date.today():
                raise forms.ValidationError("The start date must be after the date now")
        
        # Comparer les dates
        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError("The start date must be before the end date.")
        
        return cleaned_data


class Departure_resquest_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Récupérer l'utilisateur connecté
        super(Departure_resquest_form, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['beneficiary'] = forms.ModelChoiceField(
            required=True,
            widget=forms.Select(attrs={'class': 'form-control col-md-6 rounded-0', 'placeholder': 'Employé'}),
            queryset=User.objects.filter(id=user.id) if user else User.objects.none()
            )
            
            self.fields['holiday'] = forms.ModelChoiceField(
            required=True,
            widget=forms.Select(attrs={'class': 'form-control col-md-6 rounded-0', 'placeholder': 'holiday'}),
            queryset=Holiday.objects.filter(beneficiary=user.id, status='waiting') if user else Holiday.objects.none()
            )      
        
    code = forms.CharField(max_length=100,disabled=True,required=False,
                               widget=forms.TextInput({
                                   'class': 'form-control col-md-6 rounded-0 fs-4',
                                   'placeholder': 'Code'}))
    departure_date = forms.DateField(required=True, widget=forms.DateInput({
                                   'class': 'form-control col-md-6 rounded-0 fs-4',
                                   'placeholder': 'Date',
                                   'type': 'Date'
                                   }))
    return_date = forms.DateField(required=True, widget=forms.DateInput({
                                   'class': 'form-control col-md-6 rounded-0 fs-4',
                                   'placeholder': 'Date',
                                   'type': 'Date'
                                   }))
    
    
    class Meta:
        model = Departure_resquest
        fields = ['code', 'departure_date', 'return_date', 'beneficiary', 'holiday']
    
    def clean(self):
        #verification de l'ordre entre l'heure de debut et l'heure de fin (heure debut < heure de fin)
        cleaned_data = super().clean()
        departure_date = cleaned_data.get("departure_date")
        return_date = cleaned_data.get("return_date")
        
        if departure_date :
            if departure_date <= dt.date.today():
                raise forms.ValidationError("The departure date must be after the date now")
        
        # Comparer les dates
        if departure_date and return_date:
            if departure_date >= return_date:
                raise forms.ValidationError("The departure date must be before the return date.")
        
        
        return cleaned_data
    

class Validation_departure_form(forms.Form):
    Status = forms.ChoiceField(required=False, choices=(("waiting","Waiting"),("confirmed","Confirmed"),("rejected","Rejected")), widget=forms.Select({
                                   'class': 'form-control col-md-6 rounded-0',
                                   'placeholder': 'Status'}))

class Validation_Holiday(forms.Form):
    Status = forms.ChoiceField(required=False, choices=(("waiting","Waiting"),("confirmed","Confirmed"),("reported","Reported")), widget=forms.Select({
                                   'class': 'form-control col-md-6 rounded-0',
                                   'placeholder': 'Status'}))