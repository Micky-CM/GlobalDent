from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Patient, ClinicalHistory, Tooth
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Patient)
def create_history_and_teeth(sender, instance, created, **kwargs):
    """
    Cuando se guarda un nuevo Paciente (created=True),
    crea automáticamente su ClinicalHistory y sus 32 objetos Tooth (ADA 1-32).
    """
    if created:
        try:
            # Verificar si ya existe una historia (creada por el inline del admin)
            if hasattr(instance, 'history'):
                logger.info(f"ℹ️ Historia ya existe para {instance}, creando solo dientes")
                history = instance.history
            else:
                # Crear la Historia Clínica
                history = ClinicalHistory.objects.create(patient=instance)
                logger.info(f"✅ Historia Clínica creada para {instance}")

            # Verificar si ya tiene dientes antes de crearlos
            if history.teeth.exists():
                logger.info(f"ℹ️ Los dientes ya existen para {instance}")
                return

            # Generar los 32 Dientes (Sistema ADA 1 a 32)
            with transaction.atomic():
                teeth_to_create = [
                    Tooth(history=history, number_ada=i, status='S')
                    for i in range(1, 33)
                ]
                Tooth.objects.bulk_create(teeth_to_create)
                logger.info(f"✅ 32 Dientes ADA (1-32) creados para {instance}")
            
        except Exception as e:
            logger.error(
                f"❌ Error al crear historia/dientes para {instance}: {str(e)}"
            )
            raise


@receiver(post_save, sender=ClinicalHistory)
def create_teeth_if_missing(sender, instance, created, **kwargs):
    """
    Signal de respaldo: Si por alguna razón una ClinicalHistory se crea
    sin dientes, este signal los genera automáticamente.
    
    Solo crea dientes si NO existen, evitando duplicados.
    """
    # Solo ejecutar si no hay dientes
    if instance.teeth.count() == 0:
        try:
            with transaction.atomic():
                teeth_to_create = [
                    Tooth(history=instance, number_ada=i, status='S')
                    for i in range(1, 33)
                ]
                Tooth.objects.bulk_create(teeth_to_create)
                logger.info(
                    f"✅ 32 Dientes creados para historia de {instance.patient}"
                )
        except Exception as e:
            logger.error(
                f"❌ Error al crear dientes para {instance.patient}: {str(e)}"
            )
    elif instance.teeth.count() < 32:
        logger.warning(
            f"⚠️ Historia de {instance.patient} tiene solo {instance.teeth.count()} dientes"
        )