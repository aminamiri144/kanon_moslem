from django.shortcuts import render
from letters.models import Letter, Organ
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from khamka.views import LoginRequiredMixin, SuccessMessageMixin
from letters.forms import LetterForm, OrganForm, LetterUpdateForm
from django.urls import reverse


# class LetterRCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#     model = Letter
#     template_name = 'letters/create.html'
#     form_class = LetterForm
#     success_message = 'نامه جدید با موفقیت افزوده شد !'
    
#     def get_initial(self):
#         """
#         در اینجا مقدار فیلد درخواست دهنده را با توجه به ادرس مقدار دهی میکنیم 
#         """
#         customer = self.kwargs['requestid']
#         return {'request': customer}
    
#     def get_success_url(self):
#         return reverse('letter-detail', kwargs={'pk': self.object.pk,})


class LetterCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Letter
    template_name = 'letters/create.html'
    form_class = LetterForm
    success_message = 'نامه جدید با موفقیت افزوده شد !'

    def get_success_url(self):
        return reverse('letter-detail', kwargs={'pk': self.object.pk,})


class OrganCreateView(CreateView, LoginRequiredMixin, SuccessMessageMixin):
    model = Organ
    template_name = 'organ/create.html'
    success_url = '/letters/create'
    form_class = OrganForm
    success_message = 'سازمان جدید با موفقیت افزوده شد !'






class LetterListView(LoginRequiredMixin, ListView):
    paginate_by = 20
    model = Letter
    context_object_name = 'letters'
    template_name = 'letters/list.html'

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-register_date')
        return ordering

    def get_queryset(self):
        value = self.request.GET.get('q', '')
        option = self.request.GET.get('option', '')
        status = self.request.GET.get('status', '')
        if status and status != '0':
            object_list = self.model.objects.filter(status=status)
            return object_list
        else:
            query = {f'{option}__icontains': value}
            if value:
                object_list = self.model.objects.filter(**query)
                self.request.session['search'] = self.request.GET.get('q','')
            else:
                object_list = self.model.objects.all()

            return object_list
        
    def get_initial(self):
        """
        در اینجا مقدار فیلد درخواست دهنده را با توجه به ادرس مقدار دهی میکنیم 
        """
        if self.kwargs['option']:
            option = self.kwargs['option']
            return {'option': option}


class LetterDetailView(DetailView, LoginRequiredMixin):
    model = Letter
    template_name = 'letters/detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super(LetterDetailView, self).get_context_data(**kwargs)
    #     imgstr = self.object.image.name
    #     img = imgstr.split('/')
    #     imgName = img[1]
    #     context['imgname'] = imgName
    #     return context



class LetterUpdateView(UpdateView, LoginRequiredMixin, SuccessMessageMixin):
    model = Letter
    form_class = LetterUpdateForm
    template_name = 'letters/update.html'
    success_url = '/letters/'
    context_object_name = 'letters'
    success_message = "نامه با موفقیت ویرایش شد!"

    def get_success_url(self):
        return reverse('letter-detail', kwargs={'pk': self.object.pk,})

    def get_initial(self):
        """
        در اینجا مقدار فیلد درخواست دهنده را با توجه به ادرس مقدار دهی میکنیم 
        """
        regdate = Letter.objects.get(pk=self.kwargs['pk']).jd_register_date
        return {'register_date': regdate}