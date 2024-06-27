from django.contrib import admin
from .models import transfer, EmpresaTransfer, Chofer, Cliente, Usuarios, Reserva, destinos

# Register your models here.

admin.site.register(destinos)
admin.site.register(transfer)
admin.site.register(EmpresaTransfer)
admin.site.register(Chofer)
admin.site.register(Cliente)
admin.site.register(Usuarios)
admin.site.register(Reserva)
