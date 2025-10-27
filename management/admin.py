from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Patient, ClinicalHistory, Tooth, Consultation, 
    Procedure, ToothProcedure, Payment, Appointment
)

# 1. Registro simple de modelos de catálogo
@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price_formatted')
    search_fields = ('name',)
    list_per_page = 20

    @admin.display(description='Precio Base')
    def base_price_formatted(self, obj):
        return f"${obj.base_price:,.2f}"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'amount_formatted', 'method', 'payment_date')
    list_filter = ('method', 'payment_date')
    date_hierarchy = 'payment_date'
    readonly_fields = ('payment_date',)

    @admin.display(description='Monto')
    def amount_formatted(self, obj):
        return f"${obj.amount:,.2f}"

# 2. Inlines para modelos relacionados
class ToothInline(admin.TabularInline):
    """Muestra los 32 dientes dentro de la Historia Clínica."""
    model = Tooth
    fields = ('number_ada', 'status')
    readonly_fields = ('number_ada',)
    extra = 0
    can_delete = False
    max_num = 32
    # Opcional: ordenar por número ADA
    ordering = ('number_ada',)

@admin.register(ClinicalHistory)
class ClinicalHistoryAdmin(admin.ModelAdmin):
    """Muestra los campos de la Historia Clínica y sus Dientes asociados."""
    list_display = ('patient', 'opening_date', 'blood_type')
    search_fields = ('patient__first_name', 'patient__paternal_surname', 'patient__id_number')
    list_filter = ('blood_type', 'opening_date')
    inlines = [ToothInline]
    readonly_fields = ('opening_date',)
    
    fieldsets = (
        ('Información del Paciente', {
            'fields': ('patient', 'opening_date')
        }),
        ('Información Médica', {
            'fields': ('blood_type', 'preexisting_conditions', 'current_medications')
        }),
        ('Contacto de Emergencia', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone'),
            'classes': ('collapse',)
        }),
        ('Observaciones Odontológicas', {
            'fields': ('oral_health_observations',)
        }),
    )
    
    # No permitimos agregar manualmente, se crea automáticamente con señales
    def has_add_permission(self, request):
        return False


class ClinicalHistoryInline(admin.StackedInline):
    """Muestra la Historia Clínica dentro del Paciente."""
    model = ClinicalHistory
    can_delete = False
    # IMPORTANTE: max_num=1 evita que se intenten crear múltiples historias
    max_num = 1
    # NO mostrar campos vacíos, la historia se crea automáticamente por signal
    extra = 0
    fields = ('opening_date', 'blood_type', 'preexisting_conditions', 
              'current_medications', 'emergency_contact_name', 
              'emergency_contact_phone', 'oral_health_observations')
    readonly_fields = ('opening_date',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Panel principal para la gestión de Pacientes."""
    list_display = ('get_full_name', 'id_number', 'gender', 'phone_number', 'age', 'created_at')
    search_fields = ('first_name', 'paternal_surname', 'maternal_surname', 'id_number')
    list_filter = ('gender', 'created_at')
    date_hierarchy = 'created_at'
    inlines = [ClinicalHistoryInline]
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('first_name', 'paternal_surname', 'maternal_surname', 
                      'id_number', 'gender', 'date_of_birth')
        }),
        ('Información de Contacto', {
            'fields': ('phone_number', 'address')
        }),
    )

    @admin.display(description='Nombre Completo')
    def get_full_name(self, obj):
        return str(obj)

    @admin.display(description='Edad')
    def age(self, obj):
        from django.utils import timezone
        from datetime import date
        today = date.today()
        age = today.year - obj.date_of_birth.year - (
            (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
        )
        return f"{age} años"


class PaymentInline(admin.TabularInline):
    """Muestra los pagos o abonos realizados para esta consulta."""
    model = Payment
    extra = 1
    fields = ('amount', 'method', 'payment_date')
    readonly_fields = ('payment_date',)

class ToothProcedureInline(admin.TabularInline):
    """Muestra los procedimientos aplicados en esta consulta."""
    model = ToothProcedure
    extra = 1
    fields = ('tooth', 'procedure', 'price_charged', 'notes')
    readonly_fields = ('created_at',)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filtra los dientes para mostrar solo los del paciente de la consulta actual."""
        if db_field.name == "tooth":
            # Obtenemos el ID de la consulta desde la URL
            consultation_id = request.resolver_match.kwargs.get('object_id')
            if consultation_id:
                try:
                    consultation = Consultation.objects.get(pk=consultation_id)
                    # Filtramos solo los dientes del paciente de esta consulta
                    kwargs["queryset"] = Tooth.objects.filter(
                        history__patient=consultation.patient
                    ).order_by('number_ada')
                except Consultation.DoesNotExist:
                    pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    """Panel para la gestión de Consultas."""
    list_display = ('patient', 'date', 'total_cost_formatted', 'get_balance_display', 'user')
    readonly_fields = ('date', 'total_cost', 'get_balance_display')
    inlines = [ToothProcedureInline, PaymentInline]
    date_hierarchy = 'date'
    list_filter = ('user', 'date')
    search_fields = ('patient__first_name', 'patient__paternal_surname', 'patient__id_number')
    
    fieldsets = (
        ('Información de la Consulta', {
            'fields': ('patient', 'user', 'date')
        }),
        ('Detalles de la Consulta', {
            'fields': ('reason', 'notes')
        }),
        ('Información Financiera', {
            'fields': ('total_cost', 'get_balance_display'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Costo Total')
    def total_cost_formatted(self, obj):
        return f"${obj.total_cost:,.2f}"

    @admin.display(description='Saldo Pendiente')
    def get_balance_display(self, obj):
        balance = obj.get_balance()
        if balance > 0:
            return format_html(
                '<span style="color: red; font-weight: bold;">${:,.2f} PENDIENTE</span>',
                balance
            )
        elif balance < 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">${:,.2f} A FAVOR</span>',
                abs(balance)
            )
        return format_html('<span style="color: blue;">✓ Saldada</span>')

    def save_formset(self, request, form, formset, change):
        """
        Se ejecuta DESPUÉS de guardar los inlines (ToothProcedure y Payment).
        Aquí recalculamos el total_cost.
        """
        instances = formset.save(commit=True)
        
        # Si el formset es de ToothProcedure, recalculamos el costo total
        if formset.model == ToothProcedure:
            consultation = form.instance
            consultation.total_cost = consultation.calculate_total_cost()
            consultation.save(update_fields=['total_cost'])
        
        return instances

    def save_model(self, request, obj, form, change):
        """Guarda el usuario que realizó la consulta si no está asignado."""
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Panel para la gestión de Citas."""
    list_display = ('patient', 'date', 'start_time', 'end_time', 'status_badge', 'user')
    list_filter = ('status', 'date', 'user')
    search_fields = ('patient__first_name', 'patient__paternal_surname', 'reason')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información de la Cita', {
            'fields': ('patient', 'user', 'date', 'start_time', 'end_time')
        }),
        ('Detalles', {
            'fields': ('reason', 'notes', 'status')
        }),
        ('Relación con Consulta', {
            'fields': ('consultation',),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    @admin.display(description='Estado')
    def status_badge(self, obj):
        colors = {
            'P': '#FFA500',  # Naranja - Pendiente
            'C': '#4169E1',  # Azul - Confirmada
            'A': '#32CD32',  # Verde - Atendida
            'X': '#DC143C',  # Rojo - Cancelada
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#808080'),
            obj.get_status_display()
        )
    
    def save_model(self, request, obj, form, change):
        """Guarda el usuario que agendó la cita si no está asignado."""
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)