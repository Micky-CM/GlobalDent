from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Pacientes
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),

    # Consultas
    path('consultations/', views.consultation_list, name='consultation_list'),
    path('consultations/<int:pk>/', views.consultation_detail, name='consultation_detail'),
    path('consultations/create/<int:patient_pk>/', views.consultation_create, name='consultation_create'),
    path('consultations/<int:pk>/edit/', views.consultation_edit, name='consultation_edit'),

    # Procedimientos en dientes
    path('consultations/<int:consultation_pk>/add-procedure/', views.tooth_procedure_create, name='tooth_procedure_create'),
    path('tooth-procedures/<int:pk>/delete/', views.tooth_procedure_delete, name='tooth_procedure_delete'),

    # Pagos
    path('consultations/<int:consultation_pk>/add-payment/', views.payment_create, name='payment_create'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),

    # Catálogo de procedimientos
    path('procedures/', views.procedure_list, name='procedure_list'),
    path('procedures/create/', views.procedure_create, name='procedure_create'),
    path('procedures/<int:pk>/edit/', views.procedure_edit, name='procedure_edit'),
    path('procedures/<int:pk>/delete/', views.procedure_delete, name='procedure_delete'),
    
    # Citas / Agenda
    path('appointments/', views.appointment_calendar, name='appointment_calendar'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:pk>/edit/', views.appointment_edit, name='appointment_edit'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
]
