from django.views.generic.base import View
from django.shortcuts import redirect


class IdentifyRole(View):

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 1:
            return redirect('package_icd_management:package_list')
        elif request.user.user_type == 2:
            return redirect('program_management:program_list')
        elif request.user.user_type == 3:
            return redirect('package_service_management:package_list')
        elif request.user.user_type == 4:
            return redirect('hospital_service_management:hospital_list')
        elif request.user.user_type == 7:
            hospital = request.user.hospital.id
            return redirect('hospital_service_management:hospital_package_list',
                hospital=hospital)
        elif request.user.user_type == 8:
            return redirect('contract_management:contract_list')
        elif request.user.user_type == 9:
            return redirect('directory:service_list')
        elif request.user.user_type == 10:
            hospital = request.user.hospital.id
            return redirect('hospital_service_management:hospital_package_evaluation_list',
                hospital=hospital)
        elif request.user.user_type == 11:
            return redirect('contract_management:contract_hospital_list')
        elif request.user.user_type == 12:
            return redirect('package_service_management:package_evaluation_list')
        elif request.user.user_type == 13:
            return redirect('package_icd_management:package_evaluation_list')
        elif request.user.user_type == 14:
            return redirect('hospital_icd_management:hospital_list')
        elif request.user.user_type == 15:
            hospital = request.user.hospital.id
            return redirect('hospital_icd_management:hospital_package_evaluation_list',
                hospital=hospital)
        elif request.user.user_type == 16:
            return redirect('report_management:invoice_report_list')
        elif request.user.user_type == 17:
            return redirect('directory:admin_insurance')
        elif request.user.user_type == 18:
            return redirect('directory:admin_hospital')
        elif request.user.user_type == 19:
            return redirect('directory:admin_pro_medicine')
        elif request.user.user_type == 20:
            return redirect('directory:admin_pro_medicine_hospital')
        return redirect('price_list:group_service_list')
