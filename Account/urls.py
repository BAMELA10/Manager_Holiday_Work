#Define the router of application

from django.urls import path
from datetime import datetime
from .forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

app_name = "Account"

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('',
         LoginView.as_view
         (
            template_name='login.html',
            authentication_form=AuthenticationForm,
            extra_context=
            {
                'title': 'Login',
                'year' : datetime.now().year,
            }
         ),
         name='login' ),
    path('home/', home, name='Home'),
    
    
]