from django.urls import path
from .views import *

app_name = "Manage_Holidays"
urlpatterns = [
    path('all_holidays/', all_holiday, name='all_holidays'),
    path('my_holiday/', my_holidays, name='my_holiday'),
    path('reported_holidays/', all_reported_holiday, name='reported_holidays'),
    path('add_holiday/', add_holiday, name='add_holiday'),
    path('edit_holiday/<int:pk>', update_holiday, name='update_holiday'),
    path('delete_holiday/<int:pk>', delete_holiday, name='delete_holiday'),
    path('plan_reported_holiday/<int:pk>', plan_reported_holiday, name='plan_reported_holiday'),
    
    path('all_requests/', all_request_departure, name='all_request'),
    path('my_request/', my_request_departure, name='my_request'),
    path('waiting_request/', waiting_request_departure, name='waiting_request'),
    path('add_request/', add_request_departure, name='add_request'),
    path('edit_requesty/<int:pk>', update_request_departure, name='update_request'),
    path('delete_request/<int:pk>', delete_request_departure, name='delete_request'),
    
    #confirmed une demande de congé et un congé
    path('confirm_request/<int:pk>', decision_Holiday, name='decision_Holiday')
]