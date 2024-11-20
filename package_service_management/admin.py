from django.contrib import admin
from .models import Package, PackageService

admin.site.register(Package)
admin.site.register(PackageService)
