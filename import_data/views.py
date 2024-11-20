from django.shortcuts import render
from django.db import connections
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.db.models import F

from parler.utils.context import switch_language
from parler.models import TranslatableModel

from directory.models import ICD, Service, StateInsurance


import requests





class TranslateServiceView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        az_services = Service.objects.filter(
            translations__language_code='az'
        ).values_list('pk', flat=True)

        services = Service.objects.exclude(pk__in=az_services)[:50]
        service_for_trans = []
        for service in services:
            service_for_trans.append(service.title)
        IAM_TOKEN = 't1.9euelZrPjM-NkYzOl5GVmZzMnJaRl-3rnpWalJzPypfIx5WRypHNkJSQmsfl8_d8JQdd-e96BHsU_t3z9zxUBF3573oEexT-.mVx4wq6KjLqw0cjohY3-tak3l-P_5Q9eD3eM1k2B3CKNBBi3AQ6uU6CH6WL2KGgkk5m8ytvPhBnCoa0wXRX7AQ'
        folder_id = 'b1gvrp0vh2csf93om760'
        target_language = 'az'
        body = {
            "targetLanguageCode": target_language,
            "texts": service_for_trans,
            "folderId": folder_id,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(IAM_TOKEN)
        }
        response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
            json = body,
            headers = headers
        )
        response_json = response.json()
        # for service, translated_text in zip(services, response_json["translations"]):
        #     with switch_language(service, 'az'):
        #         service.title = translated_text['text']
        #         service.save()
        return render(request, 'import_data/translate.html', {'translates': services, 'response_json': response_json})

class ImportICDView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        with connections['db_03'].cursor() as cursor:
            cursor.execute(
                "SELECT id, mkb_code, mkb_name, parent_id FROM mkb_10 WHERE parent_id = '-'")
            mkbs_0 = cursor.fetchall()
            for mkb_0 in mkbs_0:
                mkb_0_id = str(mkb_0[0])
                mkb_0_obj = ICD.objects.create(title=mkb_0[2], code=mkb_0[1], parent=None)
                cursor.execute("SELECT id, mkb_code, mkb_name, parent_id FROM mkb_10 WHERE parent_id = %s",
                                        [mkb_0_id])
                mkbs_1 = cursor.fetchall()
                if mkbs_1:
                    for mkb_1 in mkbs_1:
                        mkb_1_id = str(mkb_1[0])
                        mkb_1_obj = ICD.objects.create(title=mkb_1[2], code=mkb_1[1], parent=mkb_0_obj)
                        cursor.execute("SELECT id, mkb_code, mkb_name, parent_id FROM mkb_10 WHERE parent_id = %s",
                                                [mkb_1_id])
                        mkbs_2 = cursor.fetchall()
                        if mkbs_2:
                            for mkb_2 in mkbs_2:
                                mkb_2_id = str(mkb_2[0])
                                mkb_2_obj = ICD.objects.create(title=mkb_2[2], code=mkb_2[1], parent=mkb_1_obj)
                                cursor.execute(
                                    "SELECT id, mkb_code, mkb_name, parent_id FROM mkb_10 WHERE parent_id = %s",
                                    [mkb_2_id])
                                mkbs_3 = cursor.fetchall()
                                for mkb_3 in mkbs_3:
                                    ICD.objects.create(title=mkb_3[2], code=mkb_3[1], parent=mkb_2_obj)
        return render(request, 'import_data/form.html')


class ImportServiceView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        print('test');exit();
        Service.objects.all().delete()
        with connections['db_03'].cursor() as cursor:

            cursor.execute(
                "SELECT id, code, name, parent_id FROM services_baza WHERE parent_id = '-'")
            mkbs_0 = cursor.fetchall()
            for mkb_0 in mkbs_0:
                mkb_0_id = str(mkb_0[0])
                mkb_0_obj = Service.objects.create(title=mkb_0[2], code=mkb_0[1], parent=None)
                cursor.execute("SELECT id, code, name, parent_id FROM services_baza WHERE parent_id = %s",
                                        [mkb_0_id])
                mkbs_1 = cursor.fetchall()
                if mkbs_1:
                    for mkb_1 in mkbs_1:
                        mkb_1_id = str(mkb_1[0])
                        mkb_1_obj = Service.objects.create(title=mkb_1[2], code=mkb_1[1], parent=mkb_0_obj)
                        cursor.execute("SELECT id, code, name, parent_id FROM services_baza WHERE parent_id = %s",
                                                [mkb_1_id])
                        mkbs_2 = cursor.fetchall()
                        if mkbs_2:
                            for mkb_2 in mkbs_2:
                                mkb_2_id = str(mkb_2[0])
                                mkb_2_obj = Service.objects.create(title=mkb_2[2], code=mkb_2[1], parent=mkb_1_obj)
                                cursor.execute(
                                    "SELECT id, code, name, parent_id FROM services_baza WHERE parent_id = %s",
                                    [mkb_2_id])
                                mkbs_3 = cursor.fetchall()
                                for mkb_3 in mkbs_3:
                                    Service.objects.create(title=mkb_3[2], code=mkb_3[1], parent=mkb_2_obj)
        return render(request, 'import_data/form.html')


class ImportServiceDjangoView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        ICD.objects.all().delete()
        with connections['db_8037'].cursor() as cursor:
            cursor.execute(
                "SELECT id, title, code, parent_id FROM directory_icd WHERE parent_id IS NULL")
            mkbs_0 = cursor.fetchall()
            for mkb_0 in mkbs_0:
                mkb_0_id = str(mkb_0[0])
                mkb_0_obj = ICD.objects.create(title=mkb_0[1], code=mkb_0[2], parent=None)
                cursor.execute("SELECT id, title, code, parent_id FROM directory_icd WHERE parent_id = %s",
                                        [mkb_0_id])
                mkbs_1 = cursor.fetchall()
                if mkbs_1:
                    for mkb_1 in mkbs_1:
                        mkb_1_id = str(mkb_1[0])
                        mkb_1_obj = ICD.objects.create(id=mkb_1[0], title=mkb_1[1], code=mkb_1[2], parent=mkb_0_obj)
                        cursor.execute("SELECT id, title, code, parent_id FROM directory_icd WHERE parent_id = %s",
                                                [mkb_1_id])
                        mkbs_2 = cursor.fetchall()
                        if mkbs_2:
                            for mkb_2 in mkbs_2:
                                mkb_2_id = str(mkb_2[0])
                                mkb_2_obj = ICD.objects.create(title=mkb_2[1], code=mkb_2[2], parent=mkb_1_obj)
                                cursor.execute(
                                    "SELECT id, title, code, parent_id FROM directory_icd WHERE parent_id = %s",
                                    [mkb_2_id])
                                mkbs_3 = cursor.fetchall()
                                for mkb_3 in mkbs_3:
                                    mkb_3_id = str(mkb_3[0])
                                    mkb_3_obj = ICD.objects.create(title=mkb_3[1], code=mkb_3[2], parent=mkb_2_obj)
                                    cursor.execute(
                                    "SELECT id, title, code, parent_id FROM directory_icd WHERE parent_id = %s",
                                    [mkb_3_id])
                                    mkbs_4 = cursor.fetchall()
                                    for mkb_4 in mkbs_4:
                                        mkb_4_id = str(mkb_4[0])
                                        mkb_4_obj = ICD.objects.create(title=mkb_4[1], code=mkb_4[2], parent=mkb_3_obj)
                                        cursor.execute(
                                        "SELECT id, title, code, parent_id FROM directory_icd WHERE parent_id = %s",
                                        [mkb_4_id])
                                        mkbs_5 = cursor.fetchall()
                                        for mkb_5 in mkbs_5:
                                            mkb_5_id = str(mkb_5[0])
                                            mkb_5_obj = ICD.objects.create(title=mkb_5[1], code=mkb_5[2], parent=mkb_4_obj)
                                            cursor.execute(
                                            "SELECT id, title, code, parent_id FROM directory_icd WHERE parent_id = %s",
                                            [mkb_5_id])
                                            mkbs_5 = cursor.fetchall()
                                            return render(request, 'import_data/test.html', {'test': 'test'})
        return render(request, 'import_data/test.html', {'test': mkbs_0})


class ImportStateInsuranceView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        with connections['db_8037'].cursor() as cursor:
            cursor.execute(
                "SELECT is_impossible, at_home_coefficient, primary_health_care_coefficient, clinical_diagnostic_coefficient, hospital_coefficient, service_id FROM directory_stateinsurance"
                )
            prices = cursor.fetchall()
            for price in prices:
                StateInsurance.objects.create(is_impossible=price[0], at_home_coefficient=price[1],
                        primary_health_care_coefficient=price[2], clinical_diagnostic_coefficient=price[3],
                        hospital_coefficient=price[4], service_id=price[5])
        return render(request, 'import_data/test.html', {'test': 'test'})

class ImportServiceStationarView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        with connections['db_03'].cursor() as cursor:
            cursor.execute(
                "SELECT id, code, name FROM services_baza_stationar")
            services = cursor.fetchall()
            for service in services:
                parent = Service.objects.get(сode='DХХ.ХХХ')
                Service.objects.create(title=service[2], code=service[1], parent=parent)

        return render(request, 'import_data/form.html')