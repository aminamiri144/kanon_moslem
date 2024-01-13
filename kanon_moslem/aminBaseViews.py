from django.shortcuts import render
from members.models import *
from kanon_moslem.views import LoginRequiredMixin, SuccessMessageMixin
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.hashers import make_password
from django import forms



class BaseTemplateViewAmin(TemplateView):
    PAGE_TITLE = ''
    PAGE_DESCRIPTION = ''
    template_name = None

    def get_context_data(self, **kwargs):
        context = {}
        context['page_title'] = self.PAGE_TITLE
        context['page_description'] = self.PAGE_DESCRIPTION
        return context

    


class BaseCreateViewAmin(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    PAGE_TITLE = ''
    PAGE_DESCRIPTION = ''
    ACTION_URL = ''
    BUTTON_TITLE = ''
    ACTION_URL = 'panel'
    template_name = 'base_views/create.html'
    date_field_id = 'id_date'

    def form_valid(self, form):
        try:  
            form.instance.password = make_password('12345')
            form.instance.email = 'test@example.com'
            return super().form_valid(form)
        except:
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.PAGE_TITLE
        context['page_description'] = self.PAGE_DESCRIPTION
        context['action_url'] = reverse(self.ACTION_URL)
        context['button_title'] = self.BUTTON_TITLE
        context['date_field_id'] = self.date_field_id
        return context

    # def get_success_url(self):
    #     return reverse(self.ACTION_URL, kwargs={'pk': self.object.pk, })


class BaseDetailViewAmin(View):
    PAGE_TITLE = ''
    PAGE_DESCRIPTION = ''
    model = None
    template_name = 'base_views/detail_view.html'
    fields = []
    models_property = []

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        context = {}
        fields_info = self.get_fields_info(obj)
        context['page_title'] = self.PAGE_TITLE
        context['page_description'] = self.PAGE_DESCRIPTION
        context['fields_info'] = fields_info
        return render(request, self.template_name, context=context)

    def get_fields_info(self, obj):
        fields_info = []
        for field in obj._meta.fields:

            if field.name in self.fields:
                value = getattr(obj, field.name)

                if field.name in self.models_property:
                    value = getattr(obj, f'jd_{field.name}')
                field_info = {
                    'verbosename': field.verbose_name,
                    'value': value
                }
                fields_info.append(field_info)
        return fields_info

class ListViewAmin(ListView):
    PAGE_TITLE = ''
    PAGE_DESCRIPTION = ''
    template_name = 'model_list_view.html'
    model = None
    create_button_title = None # عنوان دکمه ایجاد مدل
    create_url = None # آدرس دکمه ایجاد مدل
    fields = []
    fields_verbose = []
    actions = 'فاقد عملیات'

    def get_context_data(self, **kwargs):
        context = {}
        list_titles = []
        list_values = []
        objs = self.model.objects.all()
        for field in self.fields_verbose:
            list_titles.append(field)
        list_titles.append('عملیات')    
        for obj in objs:
            obj_value = []    
            for field_name in self.fields:
                field_id = getattr(obj, 'id')
                obj_value.append(getattr(obj, field_name))
            obj_value.append(self.actions)
            list_values.append(obj_value)

        
        context['page_title'] = self.PAGE_TITLE
        context['page_description'] = self.PAGE_DESCRIPTION
        context['create_button_title'] = self.create_button_title
        context['create_url'] = reverse(self.create_url)
        context['list_titles'] = list_titles
        context['list_values'] = list_values
        return context
#####################################################


class BaseFormKanon(forms.ModelForm):
    MODEL_VERBOSE_NAME = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label = f'{field.label} {self.MODEL_VERBOSE_NAME}'

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = f'{visible.field.label} را وارد کنید ...'


