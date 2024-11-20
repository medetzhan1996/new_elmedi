from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Customer
from .api.services import create_customer, update_customer, destroy_customer


@receiver(post_save, sender=Customer)
def post_save_customer(sender, instance: Customer, created, **kwargs):
    print('test post_save_customer......')
    if created:
        create_customer(instance)
    else:
        update_customer(instance.iin, instance)


@receiver(post_delete, sender=Customer)
def post_destroy_customer(sender, instance: Customer, **kwargs):
    destroy_customer(instance.iin)

     
