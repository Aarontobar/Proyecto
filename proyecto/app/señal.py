from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import transfer, EmpresaTransfer

@receiver(post_save, sender=transfer)
@receiver(post_delete, sender=transfer)
def update_transfers_count(sender, instance, **kwargs):
    company = instance.empresa
    if company:
        company.transfers_count = transfer.objects.filter(empresa=company).count()
        company.save()