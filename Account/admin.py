from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django import forms
from .models import *
import string as st
import random as rd

#generation of password
def gen_pwd():
    size = 8
    caractere = st.ascii_lowercase + st.digits + '!#$%&()*+,-./:;<=>?@[\]'
    pwd = "".join(rd.choice(caractere) for _ in range (size))
    return pwd

#forms for add a new user

class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, disabled=True,required=False)
    
    class Meta:
        model = User
        fields = ["email", "first_name","last_name","service"]
        
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        password = gen_pwd()
        user.set_password(password)
        print(password)
        if commit:
            user.save()
            
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = ["email", "password", "first_name","last_name","service","admin"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "first_name","last_name", "admin","date_joined","last_login","is_active","service"]
    list_filter = ["admin","service"]
    fieldsets = [
    (None, {"fields": ["email", "password"]}),
    ("Personal info", {"fields": ["first_name","last_name","service"]}),
    ("Permissions", {"fields": ["admin", "is_active","role"]}),
    ("Important dates", {"fields": ["date_joined","last_login"]})
    ]
    
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
    (
        None,
        {
            "classes": ["wide"],
            "fields": ["email","first_name","last_name", "password1","service"],
        },
    ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Service)




#admin.site.unregister(Group)