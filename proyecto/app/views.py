from django.shortcuts import render, redirect
from .models import transfer, Reserva, Cliente
from datetime import datetime

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
    transfers = transfer.objects.filter(disponible=True)[:3] 
    reserva_transfer_id = request.GET.get('reserva_transfer_id', None)
    return render(request, 'catalogo.html', {'transfers': transfers, 'reserva_transfer_id': reserva_transfer_id})


def transfers(request):
    marca = request.GET.get('marca', '')
    modelo = request.GET.get('modelo', '')
    capacidad = request.GET.get('capacidad', '')

    transfers = transfer.objects.all()

    if marca:
        transfers = transfers.filter(marca=marca)
    if modelo:
        transfers = transfers.filter(modelo=modelo)
    if capacidad:
        transfers = transfers.filter(capacidad__gte=capacidad)

    marcas = transfer.objects.values_list('marca', flat=True).distinct()
    modelos = transfer.objects.values_list('modelo', flat=True).distinct()

    context = {
        'transfers': transfers,
        'marcas': marcas,
        'modelos': modelos,
    }

    return render(request, 'transfers.html', context)

def procesar_reserva(request):
    if request.method == 'POST':
        transfer_id = request.POST.get('transfer_id')
        nombre = request.POST.get('nombre')
        rut = request.POST.get('rut')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        destino = request.POST.get('destino')
        cantidad_asientos = request.POST.get('cantidad_asientos')

        cliente, created = Cliente.objects.get_or_create(rut=rut, defaults={'nombre': nombre, 'correo': correo, 'telefono': telefono})
        transfer_utilizado = transfer.objects.get(patente=transfer_id)

        reserva = Reserva.objects.create(
            transfer_utilizado=transfer_utilizado.patente,
            cliente_id=cliente.rut,
            fecha_realizacion=datetime.strptime(fecha, '%Y-%m-%d').date(),
            hora_realizacion=datetime.strptime(hora, '%H:%M').time(),
            destino=destino,
            cantidad_asientos=cantidad_asientos
        )

        
        return redirect('confirmacion_reserva') 

    return render(request, 'error.html')  