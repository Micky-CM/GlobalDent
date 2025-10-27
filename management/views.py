from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count, F
from django.db import models
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
from .models import Patient, ClinicalHistory, Tooth, Consultation, Procedure, ToothProcedure, Payment, Appointment
from .forms import PatientForm, ClinicalHistoryForm, ConsultationForm, ProcedureForm, ToothProcedureForm, PaymentForm, AppointmentForm


# ==================== DASHBOARD ====================

@login_required
def dashboard(request):
    """Dashboard principal con estadísticas generales."""
    total_patients = Patient.objects.count()
    total_consultations = Consultation.objects.count()
    total_procedures = ToothProcedure.objects.count()
    
    # Consultas recientes
    recent_consultations = Consultation.objects.select_related('patient', 'user').order_by('-date')[:5]
    
    # Pacientes recientes
    recent_patients = Patient.objects.order_by('-created_at')[:5]
    
    # Ingresos del mes actual
    current_month = timezone.now().month
    current_year = timezone.now().year
    monthly_income = Payment.objects.filter(
        payment_date__month=current_month,
        payment_date__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    # Consultas pendientes de pago
    pending_consultations = Consultation.objects.annotate(
        total_paid=Sum('payments__amount')
    ).filter(
        Q(total_paid__lt=F('total_cost')) | Q(total_paid__isnull=True)
    ).exclude(total_cost=0)[:5]
    
    context = {
        'total_patients': total_patients,
        'total_consultations': total_consultations,
        'total_procedures': total_procedures,
        'monthly_income': monthly_income,
        'recent_consultations': recent_consultations,
        'recent_patients': recent_patients,
        'pending_consultations': pending_consultations,
    }
    return render(request, 'management/dashboard.html', context)


# ==================== PACIENTES ====================

@login_required
def patient_list(request):
    """Lista de todos los pacientes con búsqueda."""
    query = request.GET.get('q', '')
    patients = Patient.objects.all()
    
    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) |
            Q(paternal_surname__icontains=query) |
            Q(maternal_surname__icontains=query) |
            Q(id_number__icontains=query)
        )
    
    patients = patients.order_by('paternal_surname', 'first_name')
    
    context = {
        'patients': patients,
        'query': query,
    }
    return render(request, 'management/patient_list.html', context)


@login_required
def patient_detail(request, pk):
    """Detalle de un paciente con su historia clínica y consultas."""
    patient = get_object_or_404(Patient, pk=pk)
    
    try:
        history = patient.history
        teeth = history.teeth.all().order_by('number_ada')
    except ClinicalHistory.DoesNotExist:
        history = None
        teeth = []

    consultations = patient.consultations.all().order_by('-date')

    context = {
        'patient': patient,
        'history': history,
        'teeth': teeth,
        'consultations': consultations,
    }
    return render(request, 'management/patient_detail.html', context)


@login_required
def patient_create(request):
    """Crear un nuevo paciente."""
    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        history_form = ClinicalHistoryForm(request.POST)
        
        if patient_form.is_valid() and history_form.is_valid():
            patient = patient_form.save()
            
            # La historia clínica y los dientes se crean automáticamente por signals
            # Pero actualizamos los campos adicionales si se proporcionaron
            if hasattr(patient, 'history'):
                history = patient.history
                for field, value in history_form.cleaned_data.items():
                    if value:
                        setattr(history, field, value)
                history.save()
            
            messages.success(request, f'Paciente {patient} creado exitosamente.')
            return redirect('patient_detail', pk=patient.pk)
    else:
        patient_form = PatientForm()
        history_form = ClinicalHistoryForm()
    
    context = {
        'patient_form': patient_form,
        'history_form': history_form,
        'action': 'Crear',
    }
    return render(request, 'management/patient_form.html', context)


@login_required
def patient_edit(request, pk):
    """Editar un paciente existente."""
    patient = get_object_or_404(Patient, pk=pk)
    
    try:
        history = patient.history
    except ClinicalHistory.DoesNotExist:
        history = None
    
    if request.method == 'POST':
        patient_form = PatientForm(request.POST, instance=patient)
        history_form = ClinicalHistoryForm(request.POST, instance=history) if history else None
        
        if patient_form.is_valid() and (not history_form or history_form.is_valid()):
            patient_form.save()
            if history_form:
                history_form.save()
            
            messages.success(request, f'Paciente {patient} actualizado exitosamente.')
            return redirect('patient_detail', pk=patient.pk)
    else:
        patient_form = PatientForm(instance=patient)
        history_form = ClinicalHistoryForm(instance=history) if history else None
    
    context = {
        'patient_form': patient_form,
        'history_form': history_form,
        'patient': patient,
        'action': 'Editar',
    }
    return render(request, 'management/patient_form.html', context)


@login_required
def patient_delete(request, pk):
    """Eliminar un paciente."""
    patient = get_object_or_404(Patient, pk=pk)
    
    if request.method == 'POST':
        patient_name = str(patient)
        patient.delete()
        messages.success(request, f'Paciente {patient_name} eliminado exitosamente.')
        return redirect('patient_list')
    
    context = {'patient': patient}
    return render(request, 'management/patient_confirm_delete.html', context)


# ==================== CONSULTAS ====================

@login_required
def consultation_list(request):
    """Lista de todas las consultas."""
    consultations = Consultation.objects.select_related('patient', 'user').order_by('-date')
    
    context = {'consultations': consultations}
    return render(request, 'management/consultation_list.html', context)


@login_required
def consultation_detail(request, pk):
    """Detalle de una consulta con odontograma y procedimientos."""
    consultation = get_object_or_404(Consultation, pk=pk)
    tooth_procedures = consultation.tooth_procedures.select_related('tooth', 'procedure').all()
    payments = consultation.payments.all()
    
    # Calcular balance
    total_paid = payments.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    balance = consultation.total_cost - total_paid
    
    # Obtener todos los dientes del paciente para el odontograma
    try:
        teeth = consultation.patient.history.teeth.all().order_by('number_ada')
    except:
        teeth = []
    
    context = {
        'consultation': consultation,
        'tooth_procedures': tooth_procedures,
        'payments': payments,
        'total_paid': total_paid,
        'balance': balance,
        'teeth': teeth,
    }
    return render(request, 'management/consultation_detail.html', context)


@login_required
def consultation_create(request, patient_pk):
    """Crear una nueva consulta para un paciente."""
    patient = get_object_or_404(Patient, pk=patient_pk)
    
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.patient = patient
            consultation.user = request.user
            consultation.save()
            
            messages.success(request, 'Consulta creada exitosamente.')
            return redirect('consultation_detail', pk=consultation.pk)
    else:
        form = ConsultationForm()
    
    context = {
        'form': form,
        'patient': patient,
    }
    return render(request, 'management/consultation_form.html', context)


@login_required
def consultation_edit(request, pk):
    """Editar una consulta existente."""
    consultation = get_object_or_404(Consultation, pk=pk)
    
    if request.method == 'POST':
        form = ConsultationForm(request.POST, instance=consultation)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Consulta actualizada exitosamente.')
            return redirect('consultation_detail', pk=consultation.pk)
    else:
        form = ConsultationForm(instance=consultation)
    
    context = {
        'form': form,
        'consultation': consultation,
        'patient': consultation.patient,
    }
    return render(request, 'management/consultation_form.html', context)


# ==================== PROCEDIMIENTOS EN DIENTES ====================

@login_required
def tooth_procedure_create(request, consultation_pk):
    """Agregar un procedimiento a un diente en una consulta."""
    consultation = get_object_or_404(Consultation, pk=consultation_pk)
    
    if request.method == 'POST':
        form = ToothProcedureForm(request.POST, patient=consultation.patient)
        
        if form.is_valid():
            tooth_procedure = form.save(commit=False)
            tooth_procedure.consultation = consultation
            tooth_procedure.save()
            
            # Actualizar el costo total de la consulta
            consultation.total_cost = consultation.calculate_total_cost()
            consultation.save()
            
            # Actualizar el estado del diente si es necesario
            tooth = tooth_procedure.tooth
            procedure_name = tooth_procedure.procedure.name.lower()
            
            if 'extracción' in procedure_name or 'extracci' in procedure_name:
                tooth.status = 'E'
            elif 'obturación' in procedure_name or 'resina' in procedure_name:
                tooth.status = 'O'
            else:
                tooth.status = 'P'
            
            tooth.save()
            
            messages.success(request, 'Procedimiento agregado exitosamente.')
            return redirect('consultation_detail', pk=consultation.pk)
    else:
        form = ToothProcedureForm(patient=consultation.patient)
    
    context = {
        'form': form,
        'consultation': consultation,
    }
    return render(request, 'management/tooth_procedure_form.html', context)


@login_required
def tooth_procedure_delete(request, pk):
    """Eliminar un procedimiento de diente."""
    tooth_procedure = get_object_or_404(ToothProcedure, pk=pk)
    consultation = tooth_procedure.consultation
    
    if request.method == 'POST':
        tooth_procedure.delete()
        
        # Recalcular el costo total de la consulta
        consultation.total_cost = consultation.calculate_total_cost()
        consultation.save()
        
        messages.success(request, 'Procedimiento eliminado exitosamente.')
        return redirect('consultation_detail', pk=consultation.pk)
    
    context = {
        'tooth_procedure': tooth_procedure,
        'consultation': consultation,
    }
    return render(request, 'management/tooth_procedure_confirm_delete.html', context)


# ==================== PAGOS ====================

@login_required
def payment_create(request, consultation_pk):
    """Registrar un pago para una consulta."""
    consultation = get_object_or_404(Consultation, pk=consultation_pk)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        
        if form.is_valid():
            payment = form.save(commit=False)
            payment.consultation = consultation
            payment.save()
            
            messages.success(request, f'Pago de ${payment.amount} registrado exitosamente.')
            return redirect('consultation_detail', pk=consultation.pk)
    else:
        # Calcular el balance pendiente
        total_paid = consultation.payments.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        balance = consultation.total_cost - total_paid
        
        form = PaymentForm(initial={'amount': balance if balance > 0 else None})
    
    context = {
        'form': form,
        'consultation': consultation,
    }
    return render(request, 'management/payment_form.html', context)


@login_required
def payment_delete(request, pk):
    """Eliminar un pago."""
    payment = get_object_or_404(Payment, pk=pk)
    consultation = payment.consultation
    
    if request.method == 'POST':
        payment.delete()
        messages.success(request, 'Pago eliminado exitosamente.')
        return redirect('consultation_detail', pk=consultation.pk)
    
    context = {
        'payment': payment,
        'consultation': consultation,
    }
    return render(request, 'management/payment_confirm_delete.html', context)


# ==================== PROCEDIMIENTOS (CATÁLOGO) ====================

@login_required
def procedure_list(request):
    """Lista de procedimientos del catálogo."""
    procedures = Procedure.objects.all().order_by('name')
    
    context = {'procedures': procedures}
    return render(request, 'management/procedure_list.html', context)


@login_required
def procedure_create(request):
    """Crear un nuevo procedimiento en el catálogo."""
    if request.method == 'POST':
        form = ProcedureForm(request.POST)
        
        if form.is_valid():
            procedure = form.save()
            messages.success(request, f'Procedimiento "{procedure.name}" creado exitosamente.')
            return redirect('procedure_list')
    else:
        form = ProcedureForm()
    
    context = {'form': form, 'action': 'Crear'}
    return render(request, 'management/procedure_form.html', context)


@login_required
def procedure_edit(request, pk):
    """Editar un procedimiento del catálogo."""
    procedure = get_object_or_404(Procedure, pk=pk)
    
    if request.method == 'POST':
        form = ProcedureForm(request.POST, instance=procedure)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'Procedimiento "{procedure.name}" actualizado exitosamente.')
            return redirect('procedure_list')
    else:
        form = ProcedureForm(instance=procedure)
    
    context = {
        'form': form,
        'procedure': procedure,
        'action': 'Editar',
    }
    return render(request, 'management/procedure_form.html', context)


@login_required
def procedure_delete(request, pk):
    """Eliminar un procedimiento del catálogo."""
    procedure = get_object_or_404(Procedure, pk=pk)
    
    if request.method == 'POST':
        procedure_name = procedure.name
        try:
            procedure.delete()
            messages.success(request, f'Procedimiento "{procedure_name}" eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'No se puede eliminar el procedimiento porque está siendo usado en consultas.')
        return redirect('procedure_list')
    
    context = {'procedure': procedure}
    return render(request, 'management/procedure_confirm_delete.html', context)


# --- Vistas de Citas / Agenda ---

@login_required
def appointment_calendar(request):
    """Vista de calendario semanal de citas."""
    from datetime import datetime, timedelta
    
    # Obtener la semana actual o la semana especificada
    week_offset = int(request.GET.get('week', 0))
    today = datetime.now().date()
    
    # Calcular el inicio de la semana (lunes)
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=6)
    
    # Obtener citas de la semana
    appointments = Appointment.objects.filter(
        date__gte=start_of_week,
        date__lte=end_of_week,
        user=request.user
    ).select_related('patient').order_by('date', 'start_time')
    
    # Generar los 7 días de la semana
    week_days = []
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        day_appointments = appointments.filter(date=day)
        week_days.append({
            'date': day,
            'appointments': day_appointments,
            'is_today': day == today
        })
    
    # Horarios de trabajo (8:00 AM - 6:00 PM)
    work_hours = []
    for hour in range(8, 18):
        work_hours.append(f"{hour:02d}:00")
    
    context = {
        'week_days': week_days,
        'work_hours': work_hours,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'week_offset': week_offset,
        'prev_week': week_offset - 1,
        'next_week': week_offset + 1,
    }
    return render(request, 'management/appointment_calendar.html', context)


@login_required
def appointment_create(request):
    """Crear una nueva cita."""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, f'Cita agendada para {appointment.patient} el {appointment.date}.')
            return redirect('appointment_calendar')
    else:
        # Pre-llenar fecha si viene del calendario
        initial_date = request.GET.get('date')
        initial_time = request.GET.get('time')
        initial_data = {}
        if initial_date:
            initial_data['date'] = initial_date
        if initial_time:
            initial_data['start_time'] = initial_time
        form = AppointmentForm(initial=initial_data)
    
    context = {'form': form}
    return render(request, 'management/appointment_form.html', context)


@login_required
def appointment_edit(request, pk):
    """Editar una cita existente."""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada exitosamente.')
            return redirect('appointment_calendar')
    else:
        form = AppointmentForm(instance=appointment)
    
    context = {'form': form, 'appointment': appointment}
    return render(request, 'management/appointment_form.html', context)


@login_required
def appointment_delete(request, pk):
    """Eliminar una cita."""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Cita eliminada exitosamente.')
        return redirect('appointment_calendar')
    
    context = {'appointment': appointment}
    return render(request, 'management/appointment_confirm_delete.html', context)


@login_required
def appointment_detail(request, pk):
    """Ver detalle de una cita."""
    appointment = get_object_or_404(Appointment, pk=pk)
    context = {'appointment': appointment}
    return render(request, 'management/appointment_detail.html', context)
