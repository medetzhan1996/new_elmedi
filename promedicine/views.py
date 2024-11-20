import os
import pandas as pd
import tempfile

from rest_framework import generics
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from customer.models import Customer
from .models import ProfessionalExamination, ExaminationAppointment
from .forms import ProfessionalExaminationForm, ExcelUploadForm
from .serializers import ExaminationAppointmentSerializer


# Mixin программы
class ProfessionalExaminationMixin(LoginRequiredMixin):
    model = ProfessionalExamination
    success_url = reverse_lazy('promedicine:professional_examination_list')


class ProfessionalExaminationEditMixin:
    form_class = ProfessionalExaminationForm


# Список
class ProfessionalExaminationListView(ProfessionalExaminationMixin, ListView):
  context_object_name = 'results'
  template_name = 'promedicine/professional_examination/list.html'


class ProfessionalExaminationCreateView(ProfessionalExaminationMixin, ProfessionalExaminationEditMixin, CreateView):
  template_name = 'promedicine/professional_examination/create.html'


class ProfessionalExaminationImportExcelView(TemplateResponseMixin, View):
    template_name = 'promedicine/professional_examination/import_excel.html'

    def get(self, request, *args, **kwargs):
        form = ExcelUploadForm()
        context = {
            'form': form
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES['excel_file']
        # Сохраните файл во временное хранилище или в сессии
        fs = FileSystemStorage(location=tempfile.gettempdir())
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        request.session['file_path'] = file_path
        return redirect('promedicine:professional_examination_import_excel_confirm')


class ConfirmImportExcelView(TemplateResponseMixin, View):
    template_name='promedicine/professional_examination/confirm_import_excel.html'

    def get(self, request, *args, **kwargs):
        file_path = request.session.get('file_path')
        if not file_path:
            return redirect('select_file')

        # Используйте pandas для чтения Excel-файла
        data = pd.read_excel(file_path)
        # Предполагаем, что вам нужны первые 5 строк для предпросмотра
        preview_data = data.head().values.tolist()
        context = {
            'preview_data': preview_data
        }
        return self.render_to_response(context)


class ConfirmImportExcelUploadView(View):
    def post(self, request, *args, **kwargs):
        file_path = request.session.get('file_path')
        if not file_path:
            return redirect('select_file')

        df = pd.read_excel(file_path)

        # Перебираем все поля формы и определяем, какие строки следует импортировать
        rows_to_import = []
        for key, value in request.POST.items():
            if "row_include_" in key and value == "include":
                row_num = key.split('_')[-1]
                rows_to_import.append(int(row_num) - 1)  # индексы в DataFrame начинаются с 0

        for index, row in df.iterrows():
            # Если этот индекс строки не находится в списке для импорта, пропустим его
            if index not in rows_to_import:
                continue

            first_name_value = row['first_name']
            last_name_value = row['last_name']
            iin_value = row['iin']
            factory_title = row['factory']
            profession_title = row['profession']

            factory_instance = Factory.objects.get(title=factory_title)
            profession_instance = Profession.objects.get(title=profession_title)

            defaults = {
                'iin': iin_value,
                'first_name': first_name_value,
                'last_name': last_name_value,
            }

            customer, created = Customer.objects.get_or_create(iin=iin_value, defaults=defaults)
            professional_examination = ProfessionalExamination(
                factory=factory_instance,
                customer=customer,
                profession=profession_instance
            )
            professional_examination.save()

        os.remove(file_path)
        return redirect('promedicine:professional_examination_list')


class ProfessionalExaminationDeleteView(ProfessionalExaminationMixin, DeleteView):
  template_name = 'promedicine/professional_examination/delete.html'


# Обновить программу
class ProfessionalExaminationUpdateView(ProfessionalExaminationMixin, ProfessionalExaminationEditMixin, UpdateView):
    template_name = 'promedicine/professional_examination/update.html'


class ExaminationAppointmentApiListView(generics.ListCreateAPIView):
    queryset = ExaminationAppointment.objects.all()
    serializer_class = ExaminationAppointmentSerializer
