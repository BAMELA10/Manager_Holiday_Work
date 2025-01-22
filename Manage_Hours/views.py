from django.shortcuts import render, redirect, reverse
from .forms import *
from Account.models import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from Account.decorator import role_required


# Create your views here.

## Manage the planning hours of employe
@login_required()
def get_all_employe(request):
    dispo_waiting = Disponibility.objects.filter(Status="waiting")
    all_employe = User.objects.all()
    context = { 'all_employe': all_employe, "dispo_waiting": dispo_waiting}
    return render(request, 'employe.html',context)


@login_required()
def find_employe(request):
    dispo_waiting = Disponibility.objects.filter(Status="waiting")
    if not request.user.is_authenticated:
        return redirect('/')
    find_input = request.GET.get('find_input') if request.GET.get('find_input') != None else ''
    all_employe = User.objects.filter(email__istartswith=find_input, first_name__istartswith=find_input, last_name__istartswith=find_input,admin=True)[:5]
    context = { 'all_employe': all_employe, "dispo_waiting": dispo_waiting}
    return render(request,'employe.html', context)

@login_required()
@role_required(User.RH)
def get_all_hours_for_employe(request, id):
    dispo_waiting = Disponibility.objects.filter(Status="waiting")
    hours = plan_hours.objects.filter(employee=id)
    employe = User.objects.get(id=id)
    context = {
        'hours': hours,
        "dispo_waiting": dispo_waiting,
        'title':'Plan Work Time',
        'texte':'',
        'employe':employe
               }
    return render(request, 'Employe_work_plan.html', context)

@login_required()
@role_required([User.RH, User.EMPLOYEE])
def get_all_hours_for_current_user(request):
    dispo_waiting = Disponibility.objects.filter(Status="waiting")
    users = request.user.id
    hours = plan_hours.objects.filter(employee=users)
    context = {
        'hours': hours,
        "dispo_waiting": dispo_waiting,
        'title':'My Work Time',
        'texte':'',
        }
    return render(request, 'Employe_work_plan.html', context)

@login_required()
@role_required([User.RH])
def add_hours(request):
    dispo_waiting = Disponibility.objects.filter(Status="waiting")
    hours_form = Hours_form()
    if request.method == "POST":
        hours_form = Hours_form(request.POST)
        if hours_form.is_valid():
            hours_form.save()
            return redirect('Manage_Hours:Employe')
        else:
            hours_form = Hours_form(request.POST)    
    context = {'hours_form': hours_form, 'title':"Add","dispo_waiting": dispo_waiting}
    return render(request, 'add_hours.html', context)

@login_required()
@role_required([User.RH])
def update_hours(request, pk):
    dispo_waiting = Disponibility.objects.filter(Status="waiting")
    scr = plan_hours.objects.get(id=pk)
    hours_form = Hours_form(instance=scr)
    if request.method == "POST":
        hours_form = Hours_form(request.POST, instance=scr)
        if hours_form.is_valid():
            hours_form.save()
            return redirect('Manage_Hours:Employe')
        else:
            hours_form = Hours_form(request.POST) 
    context = {'hours_form': hours_form, 'title':'Update',"dispo_waiting": dispo_waiting}
    return render(request, 'add_hours.html', context)

@login_required()
@role_required([User.RH])
def delete_hours(request, pk):
    dispo_waiting = Disponibility.objects.filter(Status="waiting")
    hours = plan_hours.objects.get(id=pk)
    if request.method == 'POST':
        hours.delete()
        return redirect('Manage_Hours:Employe')
    return render(request, 'delconfirm.html')

### Manage the Disponibility of Employe

@login_required()
@role_required([User.RH, User.EMPLOYEE])
def add_disponibility(request):
    dispo_waiting = Disponibility.objects.filter(Status="waiting")
    dispo_form = Disponibility_form(user=request.user)
    if request.method == "POST":
        dispo_form = Disponibility_form(request.POST,user=request.user)
        if dispo_form.is_valid():
            dispo_form.save()
            return redirect('Manage_Hours:get_disponibilities')
        else:
            dispo_form = Disponibility_form(request.POST)
    context = {"dispo_form": dispo_form, "title":"Add", "dispo_waiting": dispo_waiting}
    return render(request, 'Disponibility/add_dispo.html', context)

@login_required()
@role_required([User.RH, User.EMPLOYEE])
def update_disponibility(request, pk):
    dispo_waiting = Disponibility.objects.filter(Status="waiting")
    source = Disponibility.objects.get(id=pk)
    dispo_form = Disponibility_form(instance=source, user=request.user)
    if request.method == "POST":
        dispo_form = Disponibility_form(request.POST, instance=source,user=request.user)
        if dispo_form.is_valid():
            dispo_form.save()
            return redirect('Manage_Hours:get_disponibilities')
        else:
            dispo_form = Disponibility_form(request.POST, instance=source)
    context = {"dispo_form": dispo_form,"title":"Update", "dispo_waiting": dispo_waiting}
    return render(request, 'Disponibility/add_dispo.html', context)

@login_required()
@role_required([User.RH, User.EMPLOYEE])
def delete_disponibility(request, pk):
    dispo_waiting = Disponibility.objects.filter(Status="waiting")
    dispo = Disponibility.objects.get(id=pk)
    if request.method == 'POST':
        dispo.delete()
        return redirect('Manage_Hours:get_disponibilities')
    return render(request, 'delconfirm.html')

@login_required()
@role_required([User.RH, User.EMPLOYEE])
def get_disponibilities(request):
    dispo = Disponibility.objects.all()
    dispo_waiting = Disponibility.objects.filter(Status="waiting")
    context = {
        "dispo": dispo, 
        "dispo_waiting": dispo_waiting,
        'title':'All availability',
        'texte':'Here it is possible to consult all the availabilities processed or awaiting processing of all registered employees',
        }
    return render(request, 'Disponibility/get_Dispo.html', context)

@login_required()
@role_required([User.RH])
def get_waiting_disponibility(request):
    dispo_waiting = Disponibility.objects.filter(Status="waiting")
    context = {
        "dispo_waiting": dispo_waiting,
               }
    return render(request, 'Disponibility/notification.html', context)

@login_required()
@role_required([User.RH, User.EMPLOYEE])
def get_disponibilties_current_user(request):
    dispo_waiting = Disponibility.objects.filter(Status="waiting")
    key = request.user.id
    print(key)
    dispo = Disponibility.objects.filter(employee=key)
    context = {
        "dispo": dispo,
        "dispo_waiting": dispo_waiting,
        'title':'My availability',
        'texte':'Check the status of all your availability.',
               }
    return render(request, 'Disponibility/get_Dispo.html', context)

@login_required()
@role_required([User.RH])
def accept_or_reject_disponibility(request, pk):
    dispo_waiting = Disponibility.objects.filter(Status="waiting")
    dispo = Disponibility.objects.get(id=pk)
    form = Validation_disponibility_form()
    form_hours = Hours_form(initial={
                                    'date_day': dispo.date_day,
                                    'start_hours': dispo.start_hours,
                                    'end_hours': dispo.end_hours,
                                    'employee': dispo.employee
                                        })
    if request.method == 'POST':
        form = Validation_disponibility_form(request.POST)
        form_hours = Hours_form(request.POST, initial={
                                            'date_day': dispo.date_day,
                                            'start_hours': dispo.start_hours,
                                            'end_hours': dispo.end_hours,
                                            'employee': dispo.employee
                                        })
        if form.is_valid():
            decision = form.cleaned_data['Status'] 
            dispo.Status = decision
            if decision == "confirmed":
                if form_hours.is_valid():
                    form_hours.save()
                    
            dispo.save()   
            return redirect('Manage_Hours:get_waiting_disponibility')
    context = {"dispo": dispo, "dispo_waiting": dispo_waiting, 'form':form, "form_hours":form_hours}
    return render( request, 'Disponibility/validation_dispo.html', context)
def dispo_waiting(request):
    dispo_waiting = Disponibility.objects.filter(Status="waiting")
    return {
        'dispo_waiting': dispo_waiting
    }
def global_variable(request):
    pass








    
