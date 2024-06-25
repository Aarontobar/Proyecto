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
    return render(request, 'catalogo.html')