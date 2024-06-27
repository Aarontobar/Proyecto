from django.shortcuts import render, redirect, get_object_or_404
from .models import transfer, Reserva, Cliente, destinos
from datetime import datetime
from django.urls import reverse
import logging
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
        transfer_utilizado = transfer.objects.get(patente=transfer_id)  # Asegúrate de usar el modelo correcto para Transfer

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
    return render(request, 'nuevo-transfer.html')

def transfer_list(request):
    zona = request.GET.get('zona')
    comuna = request.GET.get('comuna')

    transfers = transfer.objects.all()
    if zona:
        transfers = transfers.filter(zona=zona)
    if comuna:
        transfers = transfers.filter(comuna=comuna)
    zonas = transfer.objects.values_list('zona', flat=True).distinct()
    comunas = transfer.objects.filter(zona=zona).values_list('comuna', flat=True).distinct() if zona else transfer.objects.values_list('comuna', flat=True).distinct()

    context = {
        'transfers': transfers,
        'zonas': zonas,
        'comunas': comunas,
        'selected_zona': zona,
        'selected_comuna': comuna,
    }

    return render(request, 'transfers/transfer_list.html', context)

