# 🚀 Inicio Rápido - GlobalDent

## Pasos para ejecutar el proyecto

### 1. Activar entorno virtual
```bash
venv\Scripts\activate
```

### 2. Aplicar migraciones
```bash
python manage.py migrate
```

### 3. Crear superusuario
```bash
python manage.py createsuperuser
```
- Usuario: admin (o el que prefieras)
- Email: tu@email.com
- Contraseña: (tu contraseña segura)

### 4. (Opcional) Crear procedimientos de ejemplo
```bash
python manage.py shell
```

Copia y pega:
```python
from management.models import Procedure

procedimientos = [
    {"name": "Limpieza Dental", "description": "Profilaxis y limpieza profunda", "base_price": 500.00},
    {"name": "Obturación con Resina", "description": "Restauración dental con resina compuesta", "base_price": 800.00},
    {"name": "Extracción Simple", "description": "Extracción de diente sin complicaciones", "base_price": 600.00},
    {"name": "Endodoncia", "description": "Tratamiento de conducto", "base_price": 2500.00},
    {"name": "Corona Dental", "description": "Colocación de corona de porcelana", "base_price": 3500.00},
    {"name": "Blanqueamiento Dental", "description": "Blanqueamiento profesional", "base_price": 1500.00},
]

for p in procedimientos:
    Procedure.objects.create(**p)

print("✅ Procedimientos creados!")
exit()
```

### 5. Ejecutar servidor
```bash
python manage.py runserver
```

### 6. Abrir navegador
Visita: **http://127.0.0.1:8000**

---

## 📋 Primer Uso

1. **Login** con el superusuario creado
2. **Ir a Procedimientos** → Crear catálogo de tratamientos
3. **Ir a Pacientes** → Crear nuevo paciente
4. **Ver detalle del paciente** → Verificar odontograma (32 dientes creados automáticamente)
5. **Nueva Consulta** → Registrar motivo y notas
6. **Agregar Procedimiento** → Seleccionar diente y tratamiento
7. **Registrar Pago** → Ingresar monto y método

---

## 🎯 URLs Principales

- **Dashboard**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/login/
- **Pacientes**: http://127.0.0.1:8000/patients/
- **Consultas**: http://127.0.0.1:8000/consultations/
- **Procedimientos**: http://127.0.0.1:8000/procedures/
- **Admin Django**: http://127.0.0.1:8000/admin/

---

## ✨ Características Clave

- ✅ **Creación automática** de historia clínica y 32 dientes al registrar paciente
- ✅ **Odontograma visual** con colores según estado del diente
- ✅ **Cálculo automático** de costos totales de consultas
- ✅ **Control de saldo** pendiente por consulta
- ✅ **Actualización automática** del estado de dientes según procedimientos aplicados

---

## 🔧 Solución de Problemas

**Error: No module named 'django'**
```bash
pip install django
```

**Error: No such table**
```bash
python manage.py migrate
```

**Olvidé mi contraseña de superusuario**
```bash
python manage.py changepassword admin
```

---

## 📞 Soporte

Revisa el archivo `README.md` para documentación completa.
