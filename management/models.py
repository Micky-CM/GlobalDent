from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal

# --- Pacientes e Historia Clínica ---

class Patient(models.Model):
    """Información básica del paciente."""
    first_name = models.CharField(max_length=50)
    paternal_surname = models.CharField(max_length=40)
    maternal_surname = models.CharField(max_length=40, blank=True, null=True)
    id_number = models.CharField(max_length=12, unique=True, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')), default='M')
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # CORREGIDO: usar los campos correctos
        maternal = f" {self.maternal_surname}" if self.maternal_surname else ""
        return f"{self.first_name} {self.paternal_surname}{maternal}"

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['paternal_surname', 'first_name']


class ClinicalHistory(models.Model):
    """Historia clínica vinculada a un paciente."""
    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name='history'
    )

    opening_date = models.DateField(default=timezone.now)
    preexisting_conditions = models.TextField(null=True, blank=True)
    current_medications = models.TextField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=25, null=True, blank=True)
    blood_type = models.CharField(max_length=5, null=True, blank=True)
    oral_health_observations = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Historia de {self.patient}"

    class Meta:
        verbose_name = "Historia Clínica"
        verbose_name_plural = "Historias Clínicas"


# --- Dientes (Estructura ADA) ---

class Tooth(models.Model):
    """Representa uno de los 32 dientes del sistema ADA."""
    history = models.ForeignKey(
        ClinicalHistory,
        on_delete=models.CASCADE,
        related_name='teeth'
    )
    number_ada = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(32)]
    )
    STATUS_CHOICES = [
        ('S', 'Sano'),
        ('C', 'Cariado'),
        ('O', 'Obturado'),
        ('E', 'Extraído'),
        ('P', 'Pendiente de Tratamiento'),
    ]
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='S'
    )

    class Meta:
        unique_together = ('history', 'number_ada')
        verbose_name = "Diente"
        verbose_name_plural = "Dientes"
        ordering = ['history', 'number_ada']

    def __str__(self):
        return f"Diente {self.number_ada} ({self.get_status_display()}) - {self.history.patient}"


# --- Consultas y Procedimientos ---

class Consultation(models.Model):
    """Una sesión de consulta con el paciente."""
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='consultations'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='consultations',
    )
    date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(verbose_name="Motivo de la consulta")
    notes = models.TextField(blank=True, null=True, verbose_name="Notas de la exploración")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Consulta de {self.patient} - {self.date.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        ordering = ['-date']

    def calculate_total_cost(self):
        """Calcula el costo total de los procedimientos en esta consulta."""
        total = self.tooth_procedures.aggregate(
            total=models.Sum('price_charged')
        )['total'] or Decimal('0.00')
        return total

    def get_balance(self):
        """Calcula el saldo pendiente (costo total - pagos realizados)."""
        total_paid = self.payments.aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')
        return self.total_cost - total_paid


class Procedure(models.Model):
    """Catálogo de posibles procedimientos dentales."""
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Procedimiento"
        verbose_name_plural = "Procedimientos"
        ordering = ['name']


class ToothProcedure(models.Model):
    """Registro de un procedimiento aplicado a un diente en una consulta específica."""
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.CASCADE,
        related_name='tooth_procedures'
    )
    tooth = models.ForeignKey(
        Tooth,
        on_delete=models.CASCADE,
        related_name='procedures_applied'
    )
    procedure = models.ForeignKey(
        Procedure,
        on_delete=models.PROTECT
    )
    price_charged = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.procedure.name} en diente {self.tooth.number_ada}"

    class Meta:
        verbose_name = "Procedimiento en Diente"
        verbose_name_plural = "Procedimientos en Dientes"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """Al guardar, si no se especifica precio, usar el precio base del procedimiento."""
        if not self.price_charged:
            self.price_charged = self.procedure.base_price
        super().save(*args, **kwargs)


# --- Pagos ---

class Payment(models.Model):
    """Registro de un pago o abono realizado por el paciente."""
    consultation = models.ForeignKey(
        Consultation,
        on_delete=models.PROTECT,
        related_name='payments',
        help_text="El pago se asocia a la consulta donde se generó el costo."
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    METHOD_CHOICES = [
        ('E', 'Efectivo'),
        ('T', 'Tarjeta'),
        ('R', 'Transferencia'),
    ]
    method = models.CharField(max_length=1, choices=METHOD_CHOICES, default='E')

    def __str__(self):
        return f"Pago de ${self.amount} para {self.consultation.patient} - {self.payment_date.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-payment_date']


# --- Citas / Agendamiento ---

class Appointment(models.Model):
    """Citas agendadas para los pacientes."""
    STATUS_CHOICES = [
        ('P', 'Pendiente'),
        ('C', 'Confirmada'),
        ('A', 'Atendida'),
        ('X', 'Cancelada'),
    ]
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='appointments'
    )
    
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    reason = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    
    # Relación opcional con consulta (cuando la cita se convierte en consulta)
    consultation = models.OneToOneField(
        'Consultation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appointment'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.patient} - {self.date} {self.start_time}"
    
    def duration_minutes(self):
        """Calcula la duración de la cita en minutos."""
        from datetime import datetime, timedelta
        start = datetime.combine(self.date, self.start_time)
        end = datetime.combine(self.date, self.end_time)
        duration = end - start
        return int(duration.total_seconds() / 60)
    
    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['date', 'start_time']
        unique_together = [['date', 'start_time', 'user']]  # Evita citas duplicadas en el mismo horario