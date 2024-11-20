from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ContractCustomer
from .api.services import create_customer_insurance, update_customer_insurance, destroy_customer_insurance


@receiver(post_save, sender=ContractCustomer)
def post_save_contract_customer(sender, instance: ContractCustomer, created, **kwargs):
    print('test...................111111111')
    if created:
        print(create_customer_insurance(instance))
    else:
        print(update_customer_insurance(instance.number, instance))


@receiver(post_delete, sender=ContractCustomer)
def post_destroy_customer(sender, instance: ContractCustomer, **kwargs):
    destroy_customer_insurance(instance.number)

     
