from django.shortcuts import render
from .models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.decorators import login_required
from Manager_Holiday_Work.settings import BASE_DIR
from .decorator import role_required

# Create your views here.
@login_required()
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def login(request):
    assert isinstance(request, HttpRequest)
    return render(request, 'login.html')

''' def add_employe(request):
    pass '''




    