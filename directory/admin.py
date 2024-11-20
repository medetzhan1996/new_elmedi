from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from parler.admin import TranslatableAdmin
from django.contrib import admin
from .models import Service, ICD, Insurance, Insurer, Hospital, FuncStructure, StateInsurance, Form


class ServiceAdminResource(resources.ModelResource):
    parent = fields.Field(
        column_name='parent',
        attribute='parent',
        widget=ForeignKeyWidget(Service, 'title'), default=None)

    class Meta:
        model = Service
        fields = (
            'id', 'title', 'code'
        )



class ServiceAdmin(TranslatableAdmin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = [
        'title', 'code'
    ]
    search_fields = ['translations__title', 'code']
    autocomplete_fields = ['parent']
    resource_class = ServiceAdminResource


class ICDAdmin(TranslatableAdmin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'title', 'code']
    search_fields = ['translations__title', 'code']
    list_editable = ('code',)
    autocomplete_fields = ['parent']


class StateInsuranceAdminResource(resources.ModelResource):
   class Meta:
        model = StateInsurance
        fields = (
            'service', 'price', 'at_home_coefficient',
            'primary_health_care_coefficient',
            'clinical_diagnostic_coefficient', 'hospital_coefficient'
        )


class StateInsuranceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = [
        'service', 'price', 'at_home_coefficient',
        'primary_health_care_coefficient',
        'clinical_diagnostic_coefficient', 'hospital_coefficient'
    ]
    search_fields = ['service', 'code']
    list_editable = (
        'price', 'at_home_coefficient',
        'primary_health_care_coefficient',
        'clinical_diagnostic_coefficient', 'hospital_coefficient'
    )
    autocomplete_fields = ['service']
    resource_class = StateInsuranceAdminResource


class FormAdmin(TranslatableAdmin):
    list_display = ['title']


admin.site.register(StateInsurance, StateInsuranceAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ICD, ICDAdmin)
admin.site.register(Insurance)
admin.site.register(Form, FormAdmin)
admin.site.register(Insurer)
admin.site.register(Hospital)
admin.site.register(FuncStructure)









