from django.db import models
from customer.models import Customer
from invoice_management.models import Invoice


# история болезни
class AttachedDocument(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/', blank=True, null=True)
    screen = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, blank=True, null=True)
