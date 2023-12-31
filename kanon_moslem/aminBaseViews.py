from django.shortcuts import render
from members.models import *
from kanon_moslem.views import LoginRequiredMixin, SuccessMessageMixin
from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.contrib.auth.hashers import make_password



class BaseCreateViewKanon(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    PAGE_TITLE = ''
    PAGE_DESCRIPTION = ''
    ACTION_URL = ''
    BUTTON_TITLE = ''
    ACTION_URL = 'panel'
    template_name = 'base_views/create.html'

    def form_valid(self, form):
        try:  
            form.instance.password = make_password('12345')
            form.instance.email = 'test@example.com'
            return super().form_valid(form)
        except:
            pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.PAGE_TITLE
        context['page_description'] = self.PAGE_DESCRIPTION
        context['action_url'] = reverse(self.ACTION_URL)
        context['button_title'] = self.BUTTON_TITLE
        return context

    def get_success_url(self):
        return reverse(self.ACTION_URL, kwargs={'pk': self.object.pk, })


class BaseDetailView(View):
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
