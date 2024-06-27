import os
import django
from django.utils import timezone
from faker import Faker
import random
from django.db import IntegrityError, transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')

django.setup()

# Importa tus modelos de Django después de django.setup()
from app.models import transfer, EmpresaTransfer, Chofer, Cliente, Reserva, Usuarios, destinos


fake = Faker()


def crear_zonas_y_comunas():
    zonas_comunas_santiago = [
        ("Centro", "Santiago"),
        ("Centro", "Providencia"),
        ("Centro", "Las Condes"),
        ("Centro", "Ñuñoa"),
        ("Centro", "Vitacura"),
        ("Centro", "La Reina"),
        ("Centro", "Macul"),
        ("Centro", "San Joaquín"),
        ("Centro", "La Florida"),
        ("Centro", "Peñalolén"),
        ("Centro", "Lo Barnechea"),
        ("Centro", "Renca"),
        ("Centro", "Quilicura"),
        ("Centro", "Huechuraba"),
        ("Centro", "Recoleta"),
        ("Centro", "Independencia"),
        ("Centro", "Conchalí"),
        ("Centro", "La Cisterna"),
        ("Centro", "La Granja"),
        ("Centro", "San Miguel"),
        ("Centro", "Pedro Aguirre Cerda"),
        ("Centro", "Lo Espejo"),
        ("Centro", "Cerrillos"),
        ("Centro", "Estación Central"),
        ("Centro", "Quinta Normal"),
        ("Centro", "Lo Prado"),
        ("Centro", "Pudahuel"),
        ("Centro", "Maipú"),
        ("Sur", "La Pintana"),
        ("Sur", "San Bernardo"),
        ("Sur", "Pirque"),
        ("Sur", "San Ramón"),
        ("Sur", "El Bosque"),
        ("Norte", "Colina"),
        ("Norte", "Lampa"),
        ("Oeste", "Puente Alto"),
        ("Oeste", "Maipú"),
        ("Oeste", "Cerrillos"),
        ("Oeste", "Estación Central"),
        ("Oeste", "San Bernardo"),
        ("Oeste", "Pirque"),
        ("Oeste", "La Pintana"),
        ("Oeste", "San Ramón")
    ]

    for zona, comuna in zonas_comunas_santiago:
        destinos.objects.get_or_create(zona=zona, comuna=comuna)

crear_zonas_y_comunas()

marcas_reales = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'Nissan']
modelos_reales = ['SUV', 'Sedan', 'Minivan']

def crear_datos_de_prueba():
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
        nombre_chofer = fake.first_name()
        apellido_chofer = fake.last_name()
        correo_chofer = f"{nombre_chofer.lower()}.{apellido_chofer.lower()}@example.com"
        chofer = Chofer.objects.create(
            rut=str(fake.unique.random_int(min=10000000, max=99999999)) + "-" + fake.random_letter(),
            usuario=fake.user_name()[:150],
            contrasenna=fake.password()[:128],
            nombre=nombre_chofer,
            apellido=apellido_chofer,
            telefono=fake.phone_number()[:20],
            correo=correo_chofer,
            horario_entrada=fake.time(),
            horario_salida=fake.time()
        )
        choferes.append(chofer)

    # Crear clientes
    clientes = []
    for _ in range(20):
        nombre_cliente = fake.name()
        cliente = Cliente.objects.create(
            nombre=nombre_cliente,
            rut=str(fake.unique.random_int(min=10000000, max=99999999)) + "-" + fake.random_letter(),
            telefono=fake.phone_number()[:20]
        )
        clientes.append(cliente)

    # Crear transfers
    destinos_disponibles = destinos.objects.all()

    # Crear transfers
    transfers = []
    for _ in range(25):
        capacidad = random.randint(4, 10)
        # Generar una patente única para cada transferencia
        patente = None
        while not patente or transfer.objects.filter(patente=patente).exists():
            patente = fake.random_uppercase_letter() * 4 + str(fake.random_int(min=10, max=99))  # Formato: AAAA99
        
        # Seleccionar un destino aleatorio para el transfer
        destino_asignado = random.choice(destinos_disponibles) if destinos_disponibles else None

        transferencia = transfer.objects.create(
            patente=patente,
            marca=random.choice(['Toyota', 'Honda', 'Ford', 'Chevrolet', 'Nissan']),
            modelo=random.choice(['SUV', 'Sedan', 'Minivan']),
            capacidad=capacidad,
            disponible=True,
            empresa=random.choice(empresas),
            conductor=random.choice(choferes) if choferes else None,
            destino=destino_asignado  # Asignar el destino seleccionado
        )
        transfers.append(transferencia)

    return empresas, choferes, clientes, transfers

# Función para crear reservas
def crear_reservas(empresas, choferes, clientes, transfers):
    transfers = list(transfer.objects.all())
    clientes = list(Cliente.objects.all())

    try:
        with transaction.atomic():
            for _ in range(50):
                transfer_utilizado = random.choice(transfers)
                cliente = random.choice(clientes)
                
                if not transfer_utilizado.pk or not cliente.pk:
                    print(f"No se puede crear reserva, transfer o cliente no encontrado en la base de datos.")
                    continue

                if not transfer_utilizado.conductor:
                    print(f"No se puede crear reserva, el transfer {transfer_utilizado.patente} no tiene conductor asignado.")
                    continue

                try:
                    destino = transfer_utilizado.destino
                    reserva = Reserva.objects.create(
                        transfer_utilizado=transfer_utilizado,
                        cliente_rut=cliente,
                        fecha_realizacion=fake.date_between(start_date='-1y', end_date='today'),
                        hora_realizacion=fake.time(),
                        zona=destino.zona if destino else None,
                        comuna=destino.comuna if destino else None,
                        cantidad_asientos=random.randint(1, 10)
                    )
                    print(f"Reserva creada correctamente: {reserva.id_reserva}")

                except IntegrityError as e:
                    print(f"Error de integridad al crear reserva: {e}")
                    print(f"Detalles del transfer: {transfer_utilizado}")
                    print(f"Detalles del cliente: {cliente}")

    except Exception as e:
        print(f"Error al crear reservas: {e}")

empresas, choferes, clientes, transfers = crear_datos_de_prueba()
crear_reservas(empresas, choferes, clientes, transfers)

# Agregar mensaje final
print("Proceso de creación de reservas completado.")

# Crear usuarios
usuarios = []
for _ in range(5):
    nombre_usuario = fake.first_name()
    apellido_usuario = fake.last_name()
    usuario = Usuarios.objects.create(
        rut=str(fake.unique.random_int(min=10000000, max=99999999)) + "-" + fake.random_letter(),
        nombre=nombre_usuario,
        apellido=apellido_usuario,
        horario_entrada=fake.time(),
        horario_salida=fake.time(),
        rol=random.choice(['admin_aeropuerto', 'admin_empresa_transfer', 'superuser'])
    )
    usuarios.append(usuario)