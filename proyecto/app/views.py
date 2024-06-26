from django.shortcuts import render
from .models import transfer, Reserva

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
    return render(request, 'catalogo.html', {'transfers': transfers})


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
    
    # Obtener listas de valores únicos para los filtros
    marcas = transfer.objects.values_list('marca', flat=True).distinct()
    modelos = transfer.objects.values_list('modelo', flat=True).distinct()

    context = {
        'transfers': transfers,
        'marcas': marcas,
        'modelos': modelos,
    }

    return render(request, 'transfers.html', context)