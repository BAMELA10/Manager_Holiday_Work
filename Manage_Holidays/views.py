from django.shortcuts import render, redirect, reverse
from .forms import *
from Account.models import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.html import escape
from Account.decorator import role_required

# Create your views here.
@login_required()
@role_required([User.RH, User.EMPLOYEE])
def all_holiday(request):
    user = request.user.id
    holidays = Holiday.objects.all()
    context = {'holidays': holidays}
    return render(request, 'holiday/all_holidays.html', context)



@login_required()
@role_required([User.RH, User.EMPLOYEE])
def my_holidays(request):
    holidays = Holiday.objects.filter(beneficiary=request.user.id)
    context = {'holidays': holidays}
    return render(request, 'holiday/my_holiday.html', context)

@login_required()
@role_required([User.RH])
def all_reported_holiday(request):
    holidays = Holiday.objects.filter(status="reported")
    context = {'holidays': holidays}
    return render(request, 'holiday/notification.html', context)


#planifier les congés reporté
@login_required()
@role_required([User.RH])
def plan_reported_holiday(request, pk):
    holiday = Holiday.objects.get(id=pk)
    holiday.status = 'waiting'
    form = Holiday_form(instance=holiday)
    form.fields['beneficiary'].disabled = True
    if request.method == 'POST':
        form = Holiday_form(request.POST, instance=holiday)
        form.fields['beneficiary'].disabled = True
        if form.is_valid():
            form.save()
            return redirect(reverse('Manage_Holidays:all_holidays'))
        else:
            form = Holiday_form(request.POST, instance=holiday)
            form.fields['beneficiary'].disabled = True
    context = {'form': form, "title":"Report"}
    return render(request, 'holiday/add_holidays.html',context)
        
    

@login_required()
@role_required([User.RH])
def add_holiday(request):
    form = Holiday_form()
    if request.method == 'POST':
        form = Holiday_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('Manage_Holidays:all_holidays'))
        else:
            form = Holiday_form(request.POST)
    context = {'form': form, "title":"Add"}
    return render(request, 'holiday/add_holidays.html',context )
        

@login_required()
@role_required([User.RH])
def update_holiday(request, pk):
    holiday = Holiday.objects.get(id=pk)
    form = Holiday_form(instance=holiday)
    if request.method == 'POST':
        form = Holiday_form(request.POST, instance=holiday)
        if form.is_valid():
            form.save()
            return redirect(reverse('Manage_Holidays:all_holidays'))
        else:
            form = Holiday_form(request.POST)
    context = {'form': form, "title":"Update"}
    return render(request, 'holiday/add_holidays.html', context)


@login_required()
@role_required([User.RH])
def delete_holiday(request, pk):
    holiday = Holiday.objects.get(id=pk)
    if request.method == 'POST':        
        holiday.delete()
        return redirect(reverse('Manage_Holidays:all_holidays'))
    return render(request, 'delconfirm.html')

#-----------------------------------------request--------------------------

@login_required()
@role_required([User.RH, User.EMPLOYEE])
def all_request_departure(request):
    items = Departure_resquest.objects.all()
    context = {
        'items': items,
        'title':'All departure requests',
        'texte':'Consult and evaluate all requests for leave and provide a balance in the number of employees to continue the work in the company.',
        }
    return render(request, 'request/all_request.html', context)

@login_required()
@role_required([User.RH, User.EMPLOYEE])
def my_request_departure(request):
    items = Departure_resquest.objects.filter(beneficiary=request.user.id)
    context = {
        'items': items,
        'title':'My departure requests',
        'texte':'Consult your leave requests and assess your possibility of going on leave.'
        }
    return render(request, 'request/all_request.html', context)

@login_required()
@role_required([User.RH])
def waiting_request_departure(request):
    items = Departure_resquest.objects.filter(status='waiting')
    waiting_request = items
    context = {
        'items': items, 
        'current_url': escape(request.path),
        'waiting_request':waiting_request,
        'title':'Departure request pending',
        'texte':'Here you will find the departure requests awaiting decision from authorized users of the system.'
        
        }
    return render(request, 'request/notification.html', context) #BASE_DIR/'Account/templates/layout.html 


@login_required()
@role_required([User.RH, User.EMPLOYEE])
def add_request_departure(request):
    form = Departure_resquest_form(user=request.user)
    if request.method == 'POST':
        form = Departure_resquest_form(request.POST,user=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('Manage_Holidays:my_request'))
        else:
            form = Departure_resquest_form(request.POST, user=request.user)
    context = {'form': form, "title":"Add"}
    return render(request, 'request/add_request.html',context )
        

@login_required()
@role_required([User.RH, User.EMPLOYEE])
def update_request_departure(request, pk):
    items = Departure_resquest.objects.get(id=pk)
    form = Departure_resquest_form(user=request.user,instance=items)
    if request.method == 'POST':
        form = Departure_resquest_form(request.POST,user=request.user, instance=items)
        if form.is_valid():
            form.save()
            return redirect(reverse('Manage_Holidays:my_request'))
        else:
            form = Departure_resquest_form(request.POST, user=request.user)
    context = {'form': form, "title":"Update"}
    return render(request, 'request/add_request.html', context)


@login_required()
@role_required([User.RH, User.EMPLOYEE])
def delete_request_departure(request, pk):
    items = Departure_resquest.objects.get(id=pk)
    if request.method == 'POST':        
        items.delete()
        return redirect(reverse('Manage_Holidays:my_request'))
    return render(request, 'delconfirm.html')

#validation d'une demande de depart
@login_required()
@role_required([User.RH])
def decision_Holiday(request, pk):
    form = Validation_departure_form()
    request_holiday = Departure_resquest.objects.get(id=pk)
    holiday = Holiday.objects.get(id=request_holiday.holiday.id)
    if request.method == "POST":
        form = Validation_departure_form(request.POST)
        if form.is_valid():
            decision = form.cleaned_data['Status']
            if decision == 'confirmed':
                request_holiday.status = decision
                holiday.status = "confirmed"
                request_holiday.save()
                holiday.save()
                return redirect(reverse('Manage_Holidays:waiting_request'))
            else :
                request_holiday.status = decision
                request_holiday.save()
                return redirect(reverse('Manage_Holidays:waiting_request'))
    else :
        form = Validation_departure_form(request.POST)
    context = {'form': form, 'request_holiday':request_holiday}
    return render(request, 'request/validation_Holiday.html', context)

def waiting_request(request):
    waiting_request = Departure_resquest.objects.filter(status='waiting')
    return {
        'waiting_request': waiting_request
    }
                
def global_variable(request):
    return{
        'title3':'All availability',
        'texte3':'Here it is possible to consult all the availabilities processed or awaiting processing of all registered employees',
        'title3':'My availability',
        'texte3':''
    } 


