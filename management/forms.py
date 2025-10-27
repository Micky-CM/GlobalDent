from django import forms
from .models import Patient, ClinicalHistory, Consultation, Procedure, ToothProcedure, Payment, Tooth, Appointment


class PatientForm(forms.ModelForm):
    """Formulario para crear/editar pacientes."""
    
    class Meta:
        model = Patient
        fields = [
            'first_name', 'paternal_surname', 'maternal_surname',
            'id_number', 'gender', 'date_of_birth',
            'phone_number', 'address'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Nombre'
            }),
            'paternal_surname': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Apellido paterno'
            }),
            'maternal_surname': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Apellido materno'
            }),
            'id_number': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'DNI/Cédula'
            }),
            'gender': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Teléfono'
            }),
            'address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Dirección completa'
            }),
        }
        labels = {
            'first_name': 'Nombre',
            'paternal_surname': 'Apellido Paterno',
            'maternal_surname': 'Apellido Materno',
            'id_number': 'DNI/Cédula',
            'gender': 'Género',
            'date_of_birth': 'Fecha de Nacimiento',
            'phone_number': 'Teléfono',
            'address': 'Dirección',
        }


class ClinicalHistoryForm(forms.ModelForm):
    """Formulario para editar historia clínica."""
    
    class Meta:
        model = ClinicalHistory
        fields = [
            'preexisting_conditions', 'current_medications',
            'emergency_contact_name', 'emergency_contact_phone',
            'blood_type', 'oral_health_observations'
        ]
        widgets = {
            'preexisting_conditions': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Condiciones médicas preexistentes'
            }),
            'current_medications': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Medicamentos actuales'
            }),
            'emergency_contact_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Nombre del contacto de emergencia'
            }),
            'emergency_contact_phone': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Teléfono de emergencia'
            }),
            'blood_type': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Ej: O+, A-, AB+'
            }),
            'oral_health_observations': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Observaciones sobre salud bucal'
            }),
        }
        labels = {
            'preexisting_conditions': 'Condiciones Preexistentes',
            'current_medications': 'Medicamentos Actuales',
            'emergency_contact_name': 'Contacto de Emergencia',
            'emergency_contact_phone': 'Teléfono de Emergencia',
            'blood_type': 'Tipo de Sangre',
            'oral_health_observations': 'Observaciones de Salud Bucal',
        }


class ConsultationForm(forms.ModelForm):
    """Formulario para crear/editar consultas."""
    
    class Meta:
        model = Consultation
        fields = ['reason', 'notes']
        widgets = {
            'reason': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Motivo de la consulta'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 5,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Notas de la exploración y diagnóstico'
            }),
        }
        labels = {
            'reason': 'Motivo de la Consulta',
            'notes': 'Notas de la Exploración',
        }


class ProcedureForm(forms.ModelForm):
    """Formulario para crear/editar procedimientos del catálogo."""
    
    class Meta:
        model = Procedure
        fields = ['name', 'description', 'base_price']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Nombre del procedimiento'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Descripción del procedimiento'
            }),
            'base_price': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': '0.00',
                'step': '0.01'
            }),
        }
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'base_price': 'Precio Base',
        }


class ToothProcedureForm(forms.ModelForm):
    """Formulario para agregar un procedimiento a un diente."""
    
    def __init__(self, *args, **kwargs):
        patient = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar solo los dientes del paciente actual
        if patient and hasattr(patient, 'history'):
            self.fields['tooth'].queryset = Tooth.objects.filter(
                history=patient.history
            ).order_by('number_ada')
        
        # Personalizar el display de los dientes
        self.fields['tooth'].label_from_instance = lambda obj: f"Diente {obj.number_ada} ({obj.get_status_display()})"
    
    class Meta:
        model = ToothProcedure
        fields = ['tooth', 'procedure', 'price_charged', 'notes']
        widgets = {
            'tooth': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            }),
            'procedure': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            }),
            'price_charged': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Notas adicionales sobre el procedimiento'
            }),
        }
        labels = {
            'tooth': 'Diente',
            'procedure': 'Procedimiento',
            'price_charged': 'Precio Cobrado',
            'notes': 'Notas',
        }


class PaymentForm(forms.ModelForm):
    """Formulario para registrar pagos."""
    
    class Meta:
        model = Payment
        fields = ['amount', 'method']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'method': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            }),
        }
        labels = {
            'amount': 'Monto',
            'method': 'Método de Pago',
        }


class AppointmentForm(forms.ModelForm):
    """Formulario para crear y editar citas."""
    
    class Meta:
        model = Appointment
        fields = ['patient', 'date', 'start_time', 'end_time', 'reason', 'notes', 'status']
        widgets = {
            'patient': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            }),
            'reason': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Ej: Limpieza dental, Revisión general, etc.'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'placeholder': 'Notas adicionales (opcional)'
            }),
            'status': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm'
            }),
        }
        labels = {
            'patient': 'Paciente',
            'date': 'Fecha',
            'start_time': 'Hora de Inicio',
            'end_time': 'Hora de Fin',
            'reason': 'Motivo de la Cita',
            'notes': 'Notas',
            'status': 'Estado',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time:
            if end_time <= start_time:
                raise forms.ValidationError('La hora de fin debe ser posterior a la hora de inicio.')
        
        return cleaned_data
