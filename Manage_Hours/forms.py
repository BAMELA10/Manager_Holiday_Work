from .models import *
from django import forms
from Account.models import *
import datetime as dt

class Hours_form(forms.ModelForm):
    code = forms.CharField(max_length=100,disabled=True,required=False,
                               widget=forms.TextInput({
                                   'class': 'form-control col-md-6 rounded-0 fs-4',
                                   'placeholder': 'Code'}))
    date_day = forms.DateField(required=True, widget=forms.DateInput({
                                   'class': 'form-control col-md-6 rounded-0 fs-4',
                                   'placeholder': 'Date',
                                   'type': 'Date'
                                   }))
    start_hours = forms.TimeField(required=True, 
                                  widget=forms.DateInput({
                                   'class': 'form-control col-md-6 rounded-0 fs-4',
                                   'placeholder': 'Date',
                                   'type': 'Time'
                                   }, format="%H:%M"))
    end_hours = forms.TimeField(required=True, widget=forms.DateInput({
                                   'class': 'form-control col-md-6 rounded-0 fs-4',
                                   'placeholder': 'Date',
                                   'type': 'Time'
                                   }, format="%H:%M"))
    employee = forms.ModelChoiceField(required=True, widget=forms.Select({
                                   'class': 'form-control col-md-6 rounded-0',
                                   'placeholder': 'Employe'}),
                                    queryset=User.objects.all())
    class Meta:
        model = plan_hours
        fields = ['code', 'date_day',  'start_hours', 'end_hours', 'employee']
    
    def clean(self):
        #verification de l'ordre entre l'heure de debut et l'heure de fin (heure debut < heure de fin)
        cleaned_data = super().clean()
        start_hours = cleaned_data.get("start_hours")
        end_hours = cleaned_data.get("end_hours")
        date_day = cleaned_data.get('date_day')
        
        if date_day :
            if date_day <= dt.date.today():
                raise forms.ValidationError("The date must be after the date now")

        # Comparer les heures
        if start_hours and end_hours:
            if start_hours >= end_hours:
                raise forms.ValidationError("The start time must be before the end time.")
        
        return cleaned_data

class Disponibility_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Récupérer l'utilisateur connecté
        super(Disponibility_form, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['employee'] = forms.ModelChoiceField(
            required=True,
            widget=forms.Select(attrs={'class': 'form-control col-md-6 rounded-0', 'placeholder': 'Employé'}),
            queryset=User.objects.filter(id=user.id) if user else User.objects.none()
        )
            
    code = forms.CharField(max_length=100,disabled=True,required=False,
                               widget=forms.TextInput({
                                   'class': 'form-control col-md-6 rounded-0 fs-4',
                                   'placeholder': 'Code'}))
    date_day = forms.DateField(required=True, widget=forms.DateInput({
                                   'class': 'form-control col-md-6 rounded-0 fs-4',
                                   'placeholder': 'Date',
                                   'type': 'Date'
                                   }))
    Date_creation = forms.DateField(required=False, disabled=True, widget=forms.DateInput({
                                   'class': 'form-control col-md-6 rounded-0 fs-4',
                                   'placeholder': 'Date',
                                   'type': 'Date',
                                   },format="%H:%M"))
    start_hours = forms.TimeField(required=True, 
                                  widget=forms.DateInput({
                                   'class': 'form-control col-md-6 rounded-0 fs-4',
                                   'placeholder': 'Date',
                                   'type': 'Time'
                                   },format="%H:%M"))
    end_hours = forms.TimeField(required=True, widget=forms.DateInput({
                                   'class': 'form-control col-md-6 rounded-0 fs-4',
                                   'placeholder': 'Date',
                                   'type': 'Time',
                                   }, format="%H:%M"))
    
    Status = forms.ChoiceField(required=False, disabled=True, choices=(("waiting","Waiting"),("confirmed","Confirmed"),("rejected","Rejected")), widget=forms.Select({
                                   'class': 'form-control col-md-6 rounded-0',
                                   'placeholder': 'Status'}))
    
    
    
    class Meta:
        model = Disponibility
        fields = "__all__"
    
    def clean(self):
        #verification de l'ordre entre l'heure de debut et l'heure de fin (heure debut < heure de fin)
        cleaned_data = super().clean()
        start_hours = cleaned_data.get("start_hours")
        end_hours = cleaned_data.get("end_hours")
        date_day = cleaned_data.get('date_day')
        
        if date_day :
            if date_day <= dt.date.today():
                raise forms.ValidationError("The date must be after the date now")
        
        # Comparer les heures
        if start_hours and end_hours:
            if start_hours >= end_hours:
                raise forms.ValidationError("The start time must be before the end time.")
        
        return cleaned_data

class Validation_disponibility_form(forms.Form):
    Status = forms.ChoiceField(required=False, choices=(("waiting","Waiting"),("confirmed","Confirmed"),("rejected","Rejected")), widget=forms.Select({
                                   'class': 'form-control col-md-6 rounded-0',
                                   'placeholder': 'Status'}))


    
