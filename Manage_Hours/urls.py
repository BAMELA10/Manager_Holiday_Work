from django.urls import path
from .views import *

app_name = "Manage_Hours"
urlpatterns = [
    path('employes/', get_all_employe, name='Employe'),
    path('find_employe/', find_employe, name='Find employe'),
    path ('get_plan_hour/', get_all_hours_for_current_user, name='get_all_hours_for_current_user'),
    path ('get_plan_hours/<int:id>/', get_all_hours_for_employe, name='get_plan_hours'),
    path ('add_plan_hours/', add_hours, name='add_plan_hours'),
    path ('update_plan_hours/<int:pk>/', update_hours, name='update_plan_hours'),
    path ('delete_plan_hours/<int:pk>/', delete_hours, name='delete_plan_hours'),
    
    
    path ('disponibilities/', get_disponibilities, name='get_disponibilities'),
    path ('waiting_disponibilities', get_waiting_disponibility, name='get_waiting_disponibility'),
    path ('My_disponibility/', get_disponibilties_current_user, name='My_disponibility'),
    path ('add_disponibility/', add_disponibility, name='add_disponibility'),
    path ('update_disponibility/<int:pk>/', update_disponibility, name='update_disponibility'),
    path ('delete_disponibility/<int:pk>/', delete_disponibility, name='delete_disponibility'),
    path ('decision_disponibility/<int:pk>/', accept_or_reject_disponibility, name='decision_disponibility'),
]