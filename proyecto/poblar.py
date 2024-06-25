import os
import django
from django.utils import timezone
from faker import Faker
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
django.setup()

# Importa tus modelos de Django después de django.setup()
from app.models import transfer, EmpresaTransfer, Chofer, Cliente, Reserva, Usuarios

fake = Faker()

# Crear empresas de transfer
empresas = []
for _ in range(5):
    empresa = EmpresaTransfer.objects.create(
        nombre=fake.company()[:50],  # Limitar a 50 caracteres
        telefono=fake.phone_number()[:20]  # Limitar a 20 caracteres
    )
    empresas.append(empresa)

# Crear choferes
choferes = []
for _ in range(10):
    nombre_chofer = fake.first_name()[:50]  # Limitar a 50 caracteres
    apellido_chofer = fake.last_name()[:50]  # Limitar a 50 caracteres
    correo_chofer = f"{nombre_chofer.lower()}.{apellido_chofer.lower()}@example.com"[:150]  # Limitar a 150 caracteres
    chofer = Chofer.objects.create(
        rut=fake.unique.uuid4()[:12],  # Limitar a 12 caracteres
        usuario=fake.user_name()[:150],  # Limitar a 150 caracteres
        contrasenna=fake.password()[:128],  # Limitar a 128 caracteres
        nombre=nombre_chofer,
        apellido=apellido_chofer,
        telefono=fake.phone_number()[:20],  # Limitar a 20 caracteres
        correo=correo_chofer,
        horario_entrada=fake.time(),
        horario_salida=fake.time()
    )
    choferes.append(chofer)

# Crear clientes
clientes = []
for _ in range(20):
    cliente = Cliente.objects.create(
        nombre=fake.name()[:100],  # Limitar a 100 caracteres
        rut=fake.unique.uuid4()[:12],  # Limitar a 12 caracteres
        correo=fake.email()[:254],  # Limitar a 254 caracteres (límite de EmailField)
        telefono=fake.phone_number()[:20]  # Limitar a 20 caracteres
    )
    clientes.append(cliente)

# Crear transfers
transfers = []
for _ in range(25):
    capacidad = random.randint(4, 10)
    transferencia = transfer.objects.create(
        patente=fake.unique.uuid4()[:20],  # Limitar a 20 caracteres
        marca=fake.company()[:100],  # Limitar a 100 caracteres
        modelo=fake.random_element(elements=('SUV', 'Sedan', 'Minivan')),
        capacidad=capacidad,
        disponible=fake.boolean(),
        empresa=random.choice(empresas),
        conductor=random.choice(choferes) if choferes else None
    )
    transfers.append(transferencia)

# Crear reservas
for _ in range(50):
    reserva = Reserva.objects.create(
        transfer_utilizado=random.choice(transfers),
        cliente=random.choice(clientes),
        fecha_realizacion=fake.date_between(start_date='-1y', end_date='today'),
        hora_realizacion=fake.time(),
        destino=fake.address()[:200],  # Limitar a 200 caracteres
        cantidad_asientos=random.randint(1, 10)
    )

# Crear usuarios
usuarios = []
for _ in range(5):
    usuario = Usuarios.objects.create(
        rut=fake.unique.uuid4()[:12],  # Limitar a 12 caracteres
        nombre=fake.first_name()[:100],  # Limitar a 100 caracteres
        apellido=fake.last_name()[:100],  # Limitar a 100 caracteres
        horario_entrada=fake.time(),
        horario_salida=fake.time(),
        rol=random.choice(['admin_aeropuerto', 'admin_empresa_transfer', 'superuser'])
    )
    usuarios.append(usuario)