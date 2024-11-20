from django.contrib import admin
from .models import Program, Package, PackageService

admin.site.register(Program)
admin.site.register(PackageService)
admin.site.register(Package)
