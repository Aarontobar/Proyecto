from django.shortcuts import render, redirect, get_object_or_404
from .models import transfer, Reserva, Cliente, destinos, EmpresaTransfer, Chofer
from datetime import datetime
from django.urls import reverse
import logging
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


logger = logging.getLogger(__name__)
# Create your views here.
def inicio(request):

    transfers_disponibles = transfer.objects.filter(disponible=True).count()

    viajes_realizados = Reserva.objects.count()

    context = {
        'transfers_disponibles': transfers_disponibles,
        'viajes_realizados': viajes_realizados
    }

    return render(request, 'inicio.html', context)

def catalogo(request):
    zonas = destinos.objects.values_list('zona', flat=True).distinct()
    zona = request.GET.get('zona')
    comuna = request.GET.get('comuna')
    transfers = transfer.objects.filter(disponible=True)
    
    if zona:
        comunas = destinos.objects.filter(zona=zona).values_list('comuna', flat=True).distinct()
    else:
        comunas = []

    if zona and comuna:
        transfers = transfers.filter(destino__zona=zona, destino__comuna=comuna)
    elif zona:
        transfers = transfers.filter(destino__zona=zona)

    transfers = transfers[:3]
    reserva_transfer_id = request.GET.get('reserva_transfer_id', None)
    
    return render(request, 'catalogo.html', {
        'transfers': transfers,
        'reserva_transfer_id': reserva_transfer_id,
        'zonas': zonas,
        'comunas': comunas,
        'selected_zona': zona,
        'selected_comuna': comuna
    })

def transfers(request):
    marca = request.GET.get('marca', '')
    modelo = request.GET.get('modelo', '')
    capacidad = request.GET.get('capacidad', '')
    zona = request.GET.get('zona')
    comuna = request.GET.get('comuna')

    transfers = transfer.objects.all()

    if marca:
        transfers = transfers.filter(marca=marca)
    if modelo:
        transfers = transfers.filter(modelo=modelo)
    if capacidad:
        transfers = transfers.filter(capacidad__gte=capacidad)
    if zona and comuna:
        transfers = transfers.filter(destino__zona=zona, destino__comuna=comuna)
    elif zona:
        transfers = transfers.filter(destino__zona=zona)

    marcas = transfer.objects.values_list('marca', flat=True).distinct()
    modelos = transfer.objects.values_list('modelo', flat=True).distinct()
    zonas = destinos.objects.values_list('zona', flat=True).distinct()
    
    if zona:
        comunas = destinos.objects.filter(zona=zona).values_list('comuna', flat=True).distinct()
    else:
        comunas = []

    context = {
        'transfers': transfers,
        'marcas': marcas,
        'modelos': modelos,
        'zonas': zonas,
        'comunas': comunas,
        'selected_zona': zona,
        'selected_comuna': comuna,
    }

    return render(request, 'transfers.html', context)

def procesar_reserva(request):
    if request.method == 'POST':
        transfer_id = request.POST.get('transfer_id')
        nombre = request.POST.get('nombre')
        rut = request.POST.get('rut')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        cantidad_asientos = request.POST.get('cantidad_asientos')

        cliente, created = Cliente.objects.get_or_create(rut=rut, defaults={'nombre': nombre, 'correo': correo, 'telefono': telefono})
        transfer_utilizado = transfer.objects.get(patente=transfer_id) 

        fecha_actual = datetime.now().date()
        hora_actual = datetime.now().time()

        reserva = Reserva.objects.create(
            transfer_utilizado=transfer_utilizado,
            cliente_rut=cliente,
            fecha_realizacion=fecha_actual,
            hora_realizacion=hora_actual,
            cantidad_asientos=cantidad_asientos,
            zona=transfer_utilizado.destino.zona,
            comuna=transfer_utilizado.destino.comuna
        )

        return redirect('reserva', reserva_id=reserva.id_reserva)
    
    return render(request, 'error.html')

def reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id_reserva=reserva_id)
    chofer_del_transfer = reserva.transfer_utilizado.conductor
    return render(request, 'reserva.html', {'reserva': reserva, 'chofer_del_transfer': chofer_del_transfer})

def login_user(request):
    if request.method == 'POST':
        print("DEBUG: POST request received")
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"DEBUG: Username: {username}, Password: {password}")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("DEBUG: Authentication successful")
            login(request, user)
            return redirect('nuevo_transfer') 
        else:
            print("DEBUG: Authentication failed")
            messages.error(request, 'Credenciales inválidas. Por favor, inténtelo de nuevo.')
    
    return render(request, 'login.html')

@login_required
def nuevo_transfer(request):
   
    marcas = transfer.objects.order_by().values_list('marca', flat=True).distinct()
    modelo = transfer.objects.order_by().values_list('modelo', flat=True).distinct()
    empresas = EmpresaTransfer.objects.all()
    conductores = Chofer.objects.all()
    destino = destinos.objects.all()

    context = {
        'marcas': marcas,
        'modelos': modelo,
        'empresas': empresas,
        'conductores': conductores,
        'destino': destino,
    }
    return render(request, 'nuevo-transfer.html', context)

def guardar_transfer(request):
    if request.method == 'POST':
        patente = request.POST.get('patente')
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        capacidad = request.POST.get('capacidad')
        disponibilidad = request.POST.get('disponibilidad') == 'on'
        empresa_id = request.POST.get('empresa_id')
        conductor_id = request.POST.get('conductor_id') 
        destino_id = request.POST.get('destino_id')
        imagen = request.FILES.get('foto')

        print(request.FILES)

        empresa = EmpresaTransfer.objects.get(nombre = empresa_id)
        chofer = Chofer.objects.get(rut = conductor_id)
        destino = destinos.objects.get(comuna = destino_id)

        try:
            nuevo_transfer = transfer.objects.create(
                patente=patente,
                marca=marca,
                modelo=modelo,
                capacidad=capacidad,
                disponible=disponibilidad,
                empresa=empresa,
                conductor=chofer,
                destino=destino,
                foto = imagen
            )
            return redirect('nuevo', id_transfer=nuevo_transfer.patente)

        except IntegrityError:
            messages.error(request, f'La patente {patente} ya existe. Intente con una patente diferente.')
            return redirect('nuevo_transfer')
    
    return render(request, 'error.html') 


def nuevo(request, id_transfer):
    transfe = get_object_or_404(transfer, patente=id_transfer)
    return render(request, 'nuevo.html', {'transfer': transfe})