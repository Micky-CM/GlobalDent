# GlobalDent - Sistema de Gestión Dental

Sistema completo de gestión clínica para odontólogos desarrollado con Django y TailwindCSS.

## Características

### ✨ Funcionalidades Principales

- **Gestión de Pacientes**: Registro completo con datos personales e historia clínica
- **Historia Clínica**: Información médica, medicamentos, contactos de emergencia
- **Odontograma Digital**: Sistema ADA con 32 dientes, visualización del estado dental
- **Consultas**: Registro de sesiones clínicas con motivo y notas de exploración
- **Procedimientos Dentales**: Catálogo de tratamientos con precios base
- **Aplicación de Tratamientos**: Vinculación de procedimientos a dientes específicos
- **Control de Pagos**: Registro de pagos parciales o completos por consulta
- **Dashboard**: Estadísticas y resumen de actividad clínica
- **Sistema de Autenticación**: Login seguro para odontólogos

### 🦷 Flujo de Trabajo

1. **Registro de Paciente**: Se crea automáticamente su historia clínica y 32 dientes (Sistema ADA)
2. **Primera Consulta**: Registro de motivo, exploración y diagnóstico
3. **Aplicación de Tratamientos**: Selección de dientes y procedimientos realizados
4. **Registro de Pagos**: Control de abonos y saldo pendiente
5. **Consultas Posteriores**: Seguimiento continuo del paciente

## Requisitos

- Python 3.8+
- Django 5.2.7
- SQLite (incluido)

## Instalación

### 1. Clonar o descargar el proyecto

```bash
cd dental_clinic
```

### 2. Activar el entorno virtual

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias (si es necesario)

```bash
pip install django
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Crear un superusuario

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear tu usuario administrador.

### 6. Crear algunos procedimientos de ejemplo (opcional)

```bash
python manage.py shell
```

Luego ejecuta:

```python
from management.models import Procedure

procedimientos = [
    {"name": "Limpieza Dental", "description": "Profilaxis y limpieza profunda", "base_price": 500.00},
    {"name": "Obturación con Resina", "description": "Restauración dental con resina compuesta", "base_price": 800.00},
    {"name": "Extracción Simple", "description": "Extracción de diente sin complicaciones", "base_price": 600.00},
    {"name": "Endodoncia", "description": "Tratamiento de conducto", "base_price": 2500.00},
    {"name": "Corona Dental", "description": "Colocación de corona de porcelana", "base_price": 3500.00},
]

for p in procedimientos:
    Procedure.objects.create(**p)

print("Procedimientos creados exitosamente!")
exit()
```

## Ejecutar el Servidor

```bash
python manage.py runserver
```

Abre tu navegador en: **http://127.0.0.1:8000**

## Uso del Sistema

### Acceso Inicial

1. Ve a http://127.0.0.1:8000
2. Serás redirigido al login
3. Ingresa con el superusuario que creaste

### Flujo Recomendado

1. **Configurar Catálogo de Procedimientos**
   - Ve a "Procedimientos" en el menú
   - Agrega los tratamientos que ofreces con sus precios

2. **Registrar Pacientes**
   - Click en "Pacientes" → "Nuevo Paciente"
   - Completa datos personales e historia clínica
   - Los 32 dientes se crean automáticamente

3. **Crear Consulta**
   - Desde el detalle del paciente, click en "Nueva Consulta"
   - Registra motivo y notas de exploración

4. **Agregar Procedimientos**
   - En el detalle de la consulta, click en "Agregar Procedimiento"
   - Selecciona el diente y el tratamiento realizado
   - El estado del diente se actualiza automáticamente

5. **Registrar Pagos**
   - En la misma consulta, click en "Registrar Pago"
   - Ingresa el monto y método de pago
   - El sistema calcula automáticamente el saldo pendiente

## Estructura del Proyecto

```
dental_clinic/
├── globaldent/              # Configuración principal
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── management/              # Aplicación principal
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Lógica de vistas
│   ├── forms.py            # Formularios
│   ├── urls.py             # URLs de la app
│   ├── admin.py            # Configuración admin
│   ├── signals.py          # Creación automática de dientes
│   └── templates/          # Plantillas HTML
│       └── management/
│           ├── base.html
│           ├── dashboard.html
│           ├── patient_*.html
│           ├── consultation_*.html
│           └── ...
├── db.sqlite3              # Base de datos
├── manage.py
└── README.md
```

## Modelos de Datos

- **Patient**: Información del paciente
- **ClinicalHistory**: Historia clínica (OneToOne con Patient)
- **Tooth**: 32 dientes por paciente (Sistema ADA)
- **Consultation**: Sesiones de consulta
- **Procedure**: Catálogo de procedimientos
- **ToothProcedure**: Procedimientos aplicados a dientes
- **Payment**: Registro de pagos

## Tecnologías Utilizadas

- **Backend**: Django 5.2.7
- **Frontend**: TailwindCSS (CDN)
- **Base de Datos**: SQLite
- **JavaScript**: Alpine.js para interactividad
- **Iconos**: Heroicons

## Panel de Administración

Accede al panel admin de Django en: **http://127.0.0.1:8000/admin**

Desde aquí puedes gestionar todos los datos del sistema de forma avanzada.

## Características Técnicas

- ✅ Signals para creación automática de historia clínica y dientes
- ✅ Cálculo automático de costos totales de consultas
- ✅ Actualización automática del estado de dientes según procedimientos
- ✅ Control de saldo pendiente por consulta
- ✅ Sistema de autenticación integrado
- ✅ Interfaz responsive con TailwindCSS
- ✅ Mensajes de confirmación y validación
- ✅ Búsqueda de pacientes

## Próximas Mejoras (Sugerencias)

- [ ] Reportes en PDF de consultas
- [ ] Calendario de citas
- [ ] Recordatorios por email/SMS
- [ ] Gráficas de estadísticas
- [ ] Exportación de datos
- [ ] Historial de cambios en odontograma
- [ ] Imágenes radiográficas
- [ ] Múltiples clínicas/sucursales

## Soporte

Para dudas o problemas, revisa:
- Modelos en `management/models.py`
- Vistas en `management/views.py`
- Plantillas en `management/templates/management/`

## Licencia

Proyecto educativo/profesional para gestión de clínicas dentales.
