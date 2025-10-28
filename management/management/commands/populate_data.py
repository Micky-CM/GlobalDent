"""
Script para poblar la base de datos con datos de prueba realistas.
Uso: python manage.py populate_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta, time
from decimal import Decimal
import random

from management.models import (
    Patient, ClinicalHistory, Tooth, Consultation, 
    Procedure, ToothProcedure, Payment, Appointment
)


class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba realistas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina todos los datos existentes antes de poblar',
        )

    def handle(self, *args, **kwargs):
        clear_data = kwargs.get('clear', False)
        
        if clear_data:
            self.stdout.write(self.style.WARNING('>> Eliminando datos existentes...'))
            self.clear_existing_data()
        
        self.stdout.write(self.style.SUCCESS('>> Iniciando poblacion de datos...'))
        
        # Crear usuario si no existe
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@globaldent.com',
                'first_name': 'Dr. Juan',
                'last_name': 'Pérez',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS('[OK] Usuario admin creado'))
        
        # Crear procedimientos
        self.create_procedures()
        
        # Crear pacientes con sus datos completos
        self.create_patients_with_data(user)
        
        self.stdout.write(self.style.SUCCESS('[OK] Poblacion de datos completada exitosamente!'))
        self.print_summary()

    def clear_existing_data(self):
        """Elimina todos los datos de prueba."""
        Payment.objects.all().delete()
        ToothProcedure.objects.all().delete()
        Appointment.objects.all().delete()
        Consultation.objects.all().delete()
        Tooth.objects.all().delete()
        ClinicalHistory.objects.all().delete()
        Patient.objects.all().delete()
        Procedure.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('[OK] Datos eliminados'))

    def create_procedures(self):
        """Crea el catálogo de procedimientos dentales."""
        procedures_data = [
            ('Limpieza Dental', 'Profilaxis y eliminación de placa bacteriana', Decimal('350.00')),
            ('Extracción Simple', 'Extracción de diente sin complicaciones', Decimal('500.00')),
            ('Extracción Compleja', 'Extracción quirúrgica de diente', Decimal('1200.00')),
            ('Obturación (Resina)', 'Restauración dental con resina compuesta', Decimal('600.00')),
            ('Obturación (Amalgama)', 'Restauración dental con amalgama', Decimal('450.00')),
            ('Endodoncia Unirradicular', 'Tratamiento de conducto en diente de una raíz', Decimal('2500.00')),
            ('Endodoncia Multirradicular', 'Tratamiento de conducto en diente de múltiples raíces', Decimal('3500.00')),
            ('Corona de Porcelana', 'Prótesis fija de porcelana', Decimal('4500.00')),
            ('Corona de Metal-Porcelana', 'Prótesis fija de metal con porcelana', Decimal('3800.00')),
            ('Blanqueamiento Dental', 'Aclaramiento del color de los dientes', Decimal('2800.00')),
            ('Implante Dental', 'Colocación de implante de titanio', Decimal('4800.00')),
            ('Puente Fijo 3 Unidades', 'Prótesis fija de 3 piezas', Decimal('4900.00')),
            ('Ortodoncia (Mensualidad)', 'Pago mensual de tratamiento ortodóntico', Decimal('1500.00')),
            ('Radiografía Periapical', 'Radiografía de diente individual', Decimal('150.00')),
            ('Radiografía Panorámica', 'Radiografía de toda la boca', Decimal('400.00')),
            ('Sellador de Fosas', 'Prevención de caries en molares', Decimal('250.00')),
            ('Aplicación de Flúor', 'Tratamiento preventivo con flúor', Decimal('200.00')),
            ('Consulta General', 'Revisión y diagnóstico general', Decimal('300.00')),
            ('Urgencia Dental', 'Atención de emergencia', Decimal('800.00')),
            ('Curetaje Dental', 'Limpieza profunda de encías', Decimal('1200.00')),
        ]
        
        for name, description, price in procedures_data:
            Procedure.objects.get_or_create(
                name=name,
                defaults={'description': description, 'base_price': price}
            )
        
        self.stdout.write(self.style.SUCCESS(f'[OK] {len(procedures_data)} procedimientos creados'))

    def create_patients_with_data(self, user):
        """Crea pacientes con historias clínicas, consultas, citas y pagos."""
        patients_data = [
            {
                'first_name': 'María', 'paternal_surname': 'González', 'maternal_surname': 'López',
                'id_number': '12345678', 'gender': 'F', 'date_of_birth': '1985-03-15',
                'phone_number': '555-0101', 'address': 'Av. Principal 123, Col. Centro'
            },
            {
                'first_name': 'Carlos', 'paternal_surname': 'Rodríguez', 'maternal_surname': 'Martínez',
                'id_number': '23456789', 'gender': 'M', 'date_of_birth': '1990-07-22',
                'phone_number': '555-0102', 'address': 'Calle Reforma 456, Col. Juárez'
            },
            {
                'first_name': 'Ana', 'paternal_surname': 'Hernández', 'maternal_surname': 'García',
                'id_number': '34567890', 'gender': 'F', 'date_of_birth': '1978-11-30',
                'phone_number': '555-0103', 'address': 'Blvd. Insurgentes 789, Col. Roma'
            },
            {
                'first_name': 'Luis', 'paternal_surname': 'Martínez', 'maternal_surname': 'Sánchez',
                'id_number': '45678901', 'gender': 'M', 'date_of_birth': '1995-05-18',
                'phone_number': '555-0104', 'address': 'Av. Universidad 321, Col. Del Valle'
            },
            {
                'first_name': 'Patricia', 'paternal_surname': 'López', 'maternal_surname': 'Ramírez',
                'id_number': '56789012', 'gender': 'F', 'date_of_birth': '1982-09-25',
                'phone_number': '555-0105', 'address': 'Calle Morelos 654, Col. Centro'
            },
            {
                'first_name': 'Roberto', 'paternal_surname': 'García', 'maternal_surname': 'Torres',
                'id_number': '67890123', 'gender': 'M', 'date_of_birth': '1988-02-14',
                'phone_number': '555-0106', 'address': 'Av. Revolución 987, Col. Mixcoac'
            },
            {
                'first_name': 'Laura', 'paternal_surname': 'Pérez', 'maternal_surname': 'Flores',
                'id_number': '78901234', 'gender': 'F', 'date_of_birth': '1992-12-08',
                'phone_number': '555-0107', 'address': 'Calle Hidalgo 147, Col. Polanco'
            },
            {
                'first_name': 'Jorge', 'paternal_surname': 'Sánchez', 'maternal_surname': 'Morales',
                'id_number': '89012345', 'gender': 'M', 'date_of_birth': '1975-06-20',
                'phone_number': '555-0108', 'address': 'Av. Constitución 258, Col. Condesa'
            },
            {
                'first_name': 'Sofía', 'paternal_surname': 'Ramírez', 'maternal_surname': 'Cruz',
                'id_number': '90123456', 'gender': 'F', 'date_of_birth': '1998-04-12',
                'phone_number': '555-0109', 'address': 'Blvd. Juárez 369, Col. Narvarte'
            },
            {
                'first_name': 'Miguel', 'paternal_surname': 'Torres', 'maternal_surname': 'Ruiz',
                'id_number': '01234567', 'gender': 'M', 'date_of_birth': '1980-08-05',
                'phone_number': '555-0110', 'address': 'Calle Independencia 741, Col. San Ángel'
            },
        ]
        
        for patient_data in patients_data:
            # Crear paciente (el signal creará automáticamente la historia clínica y dientes)
            patient = Patient.objects.create(
                first_name=patient_data['first_name'],
                paternal_surname=patient_data['paternal_surname'],
                maternal_surname=patient_data['maternal_surname'],
                id_number=patient_data['id_number'],
                gender=patient_data['gender'],
                date_of_birth=datetime.strptime(patient_data['date_of_birth'], '%Y-%m-%d').date(),
                phone_number=patient_data['phone_number'],
                address=patient_data['address']
            )
            
            # Actualizar historia clínica con datos adicionales
            self.update_clinical_history(patient)
            
            # Crear consultas con procedimientos y pagos
            self.create_consultations(patient, user)
            
            # Crear citas
            self.create_appointments(patient, user)
            
            self.stdout.write(self.style.SUCCESS(f'[OK] Paciente creado: {patient}'))

    def update_clinical_history(self, patient):
        """Actualiza la historia clínica del paciente con datos adicionales."""
        conditions = [
            'Ninguna',
            'Diabetes tipo 2 controlada',
            'Hipertensión arterial',
            'Asma',
            'Ninguna condición preexistente',
        ]
        
        medications = [
            'Ninguno',
            'Metformina 850mg',
            'Losartán 50mg',
            'Salbutamol inhalador',
            'No toma medicamentos',
        ]
        
        blood_types = ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-']
        
        # Obtener la historia clínica creada por el signal
        history = patient.history
        history.opening_date = timezone.now().date() - timedelta(days=random.randint(30, 365))
        history.preexisting_conditions = random.choice(conditions)
        history.current_medications = random.choice(medications)
        history.emergency_contact_name = f'{random.choice(["Juan", "María", "Pedro", "Ana"])} {random.choice(["Pérez", "López", "García"])}'
        history.emergency_contact_phone = f'555-{random.randint(1000, 9999)}'
        history.blood_type = random.choice(blood_types)
        history.oral_health_observations = 'Higiene oral regular. Requiere seguimiento.'
        history.save()
        
        # Actualizar algunos dientes con estados variados
        teeth = list(history.teeth.all())
        tooth_statuses = ['C', 'O', 'P', 'E']
        # Cambiar el estado de algunos dientes aleatoriamente
        for _ in range(random.randint(2, 8)):
            tooth = random.choice(teeth)
            tooth.status = random.choice(tooth_statuses)
            tooth.save()

    def create_consultations(self, patient, user):
        """Crea consultas con procedimientos y pagos para el paciente."""
        num_consultations = random.randint(1, 3)
        
        procedures = list(Procedure.objects.all())
        teeth = list(patient.history.teeth.all())
        
        for i in range(num_consultations):
            # Fecha de consulta en los últimos 6 meses
            days_ago = random.randint(7, 180)
            consultation_date = timezone.now() - timedelta(days=days_ago)
            
            reasons = [
                'Dolor en molar inferior',
                'Revisión general',
                'Limpieza dental',
                'Seguimiento de tratamiento',
                'Urgencia por dolor agudo',
                'Consulta de ortodoncia',
                'Cambio de color en diente',
                'Sensibilidad dental',
            ]
            
            consultation = Consultation.objects.create(
                patient=patient,
                user=user,
                reason=random.choice(reasons),
                notes=f'Paciente presenta {random.choice(["buena", "regular", "mala"])} higiene oral. {random.choice(["Se recomienda seguimiento.", "Requiere tratamiento adicional.", "Evolución favorable."])}',
                total_cost=Decimal('0.00')
            )
            consultation.date = consultation_date
            consultation.save()
            
            # Agregar 1-3 procedimientos a la consulta
            num_procedures = random.randint(1, 3)
            total_cost = Decimal('0.00')
            
            for _ in range(num_procedures):
                procedure = random.choice(procedures)
                tooth = random.choice(teeth)
                
                # Precio con variación del ±10%
                variation = Decimal(random.uniform(0.9, 1.1))
                price = (procedure.base_price * variation).quantize(Decimal('0.01'))
                
                ToothProcedure.objects.create(
                    consultation=consultation,
                    tooth=tooth,
                    procedure=procedure,
                    price_charged=price,
                    notes=f'Procedimiento realizado satisfactoriamente en diente {tooth.number_ada}'
                )
                
                total_cost += price
                
                # Actualizar estado del diente según procedimiento
                if 'Extracción' in procedure.name:
                    tooth.status = 'E'
                elif 'Obturación' in procedure.name:
                    tooth.status = 'O'
                tooth.save()
            
            consultation.total_cost = total_cost
            consultation.save()
            
            # Crear pagos (algunos completos, otros parciales)
            self.create_payments(consultation)

    def create_payments(self, consultation):
        """Crea pagos para una consulta."""
        payment_methods = ['E', 'T', 'R']
        
        # 70% de probabilidad de pago completo
        if random.random() < 0.7:
            # Pago completo
            Payment.objects.create(
                consultation=consultation,
                amount=consultation.total_cost,
                method=random.choice(payment_methods)
            )
        else:
            # Pagos parciales
            remaining = consultation.total_cost
            num_payments = random.randint(1, 3)
            
            for i in range(num_payments):
                if i == num_payments - 1:
                    # Último pago: puede quedar saldo pendiente
                    amount = remaining * Decimal(random.uniform(0.3, 0.8))
                else:
                    amount = remaining * Decimal(random.uniform(0.3, 0.6))
                
                amount = amount.quantize(Decimal('0.01'))
                
                Payment.objects.create(
                    consultation=consultation,
                    amount=amount,
                    method=random.choice(payment_methods)
                )
                
                remaining -= amount
                if remaining <= 0:
                    break

    def create_appointments(self, patient, user):
        """Crea citas para el paciente."""
        num_appointments = random.randint(2, 4)
        
        statuses = ['P', 'C', 'A', 'X']
        status_weights = [0.3, 0.4, 0.2, 0.1]  # Probabilidades
        
        reasons = [
            'Limpieza dental',
            'Revisión general',
            'Seguimiento de tratamiento',
            'Extracción programada',
            'Colocación de corona',
            'Ajuste de ortodoncia',
            'Endodoncia',
            'Consulta de urgencia',
        ]
        
        for i in range(num_appointments):
            # Mezcla de citas pasadas y futuras
            if i < num_appointments // 2:
                # Citas pasadas (últimos 2 meses)
                days_offset = -random.randint(1, 60)
                status = random.choices(statuses, weights=[0.1, 0.2, 0.6, 0.1])[0]
            else:
                # Citas futuras (próximos 2 meses)
                days_offset = random.randint(1, 60)
                status = random.choices(statuses, weights=[0.5, 0.4, 0.0, 0.1])[0]
            
            appointment_date = timezone.now().date() + timedelta(days=days_offset)
            
            # Horarios de 8:00 AM a 5:00 PM
            start_hour = random.randint(8, 16)
            start_minute = random.choice([0, 30])
            start_time = time(start_hour, start_minute)
            
            # Duración: 30 minutos a 2 horas
            duration_minutes = random.choice([30, 60, 90, 120])
            end_datetime = datetime.combine(appointment_date, start_time) + timedelta(minutes=duration_minutes)
            end_time = end_datetime.time()
            
            try:
                Appointment.objects.create(
                    patient=patient,
                    user=user,
                    date=appointment_date,
                    start_time=start_time,
                    end_time=end_time,
                    reason=random.choice(reasons),
                    notes=f'Cita programada para {random.choice(reasons).lower()}',
                    status=status
                )
            except:
                # Si hay conflicto de horario, continuar
                pass

    def print_summary(self):
        """Imprime un resumen de los datos creados."""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('RESUMEN DE DATOS CREADOS'))
        self.stdout.write('='*60)
        self.stdout.write(f'Pacientes: {Patient.objects.count()}')
        self.stdout.write(f'Historias Clinicas: {ClinicalHistory.objects.count()}')
        self.stdout.write(f'Dientes registrados: {Tooth.objects.count()}')
        self.stdout.write(f'Consultas: {Consultation.objects.count()}')
        self.stdout.write(f'Procedimientos aplicados: {ToothProcedure.objects.count()}')
        self.stdout.write(f'Pagos registrados: {Payment.objects.count()}')
        self.stdout.write(f'Citas agendadas: {Appointment.objects.count()}')
        self.stdout.write(f'Procedimientos en catalogo: {Procedure.objects.count()}')
        self.stdout.write('='*60 + '\n')
