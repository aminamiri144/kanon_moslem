from django.shortcuts import render
from education_management.models import *
from kanon_moslem.aminBaseViews import *
from education_management.forms import *


class TermModalCreateView(BaseCreateViewAmin):
    model = Term
    form_class = TermCreateForm
    success_message = 'ترم جدید با موفقیت افزوده شد !'
    PAGE_TITLE = 'افزودن ترم جدید'
    ACTION_URL = 'term-add'
    BUTTON_TITLE = "اضافه کردن ترم"

    def get_success_url(self):
        return reverse('term-view')

class TermModelView(ListViewAmin):
    model= Term
    PAGE_TITLE = "امور آموزشی"
    PAGE_DESCRIPTION = 'مدیریت ترم های تحصیلی'
    create_button_title = 'افزودن ترم تحصیلی' 
    create_url = 'term-add' 
    fields_verbose = ['شناسه','عنوان ترم','ترم فعال']
    fields = ['id', 'get_full_title', 'get_is_active']  


class LessonModalCreateView(BaseCreateViewAmin):
    model = Lesson
    form_class = LessonCreateForm
    success_message = 'درس جدید با موفقیت افزوده شد !'
    PAGE_TITLE = 'افزودن درس جدید'
    ACTION_URL = 'lesson-view'
    BUTTON_TITLE = "اضافه کردن درس"


    def get_success_url(self):
        return reverse('lesson-view')

class LessonModelView(ListViewAmin):
    model= Lesson
    PAGE_TITLE = "امور آموزشی"
    PAGE_DESCRIPTION = 'مدیریت درس ها'
    create_button_title = 'افزودن درس جدید' 
    create_url = 'lesson-add' 
    fields_verbose = ['شناسه','نام درس','نوع درس', 'توضیحات', 'ضریب نمره']
    fields = ['id', 'title', 'lesson_type', 'description', 'ratio'] 



class StudentDisciplineGradeListView(LoginRequiredMixin, ListView):
    paginate_by = 20
    model = DisciplineGrade
    # context_object_name = 'dgs'
    template_name = 'enzebati/enzebati_list.html'

    def get_queryset(self):
        # value = self.request.GET.get('q', '')
        # option = self.request.GET.get('option', '')
        # query = {f'{option}__icontains': value}
        # if value:
        #     object_list = self.model.objects.filter(**query)
        #     self.request.session['search'] = self.request.GET.get('q','')
        # else:
        s = Student.objects.get(pk=self.kwargs['pk'])
        # query = {'id': self.kwargs['pk']}
        object_list = self.model.objects.filter(student=s)
        return object_list
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        s = Student.objects.get(pk=self.kwargs['pk'])
        context['student_id'] = s.id
        context['student_fullname'] = s.get_full_name()
        return context

class SdgCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = DisciplineGrade
    template_name = 'enzebati/sdg_add.html'
    success_url = '/requestions/'
    form_class = DisciplineGradeCreateForm
    success_message = "درخواست جدید با موفقیت افزوده شد !"

    def get_context_data(self, **kwargs):
        """در اینجا فیلد کاستومر یا درخواست دهنده را طوری تنظیم میکنیم که 
        فقط درخواست دهنده ای که میخواهیم براش درخواست ثبت کنیم نمایش داده بشه
        و طوره نباشه که همه درخواست دهنده ها در اپشن های فیلد سلکت نمایش داده بشن
        """
        t = Term.objects.get(is_active=True)
        # context = super().get_context_data(**kwargs)
        context = super(SdgCreateView, self).get_context_data(**kwargs)
        context['form'].fields['student'].choices.field.queryset = Student.objects.filter(pk=self.kwargs['pk'])
        context['form'].fields['term'].choices.field.queryset = Term.objects.filter(is_active=True)
        context['student_id'] = self.kwargs['pk']
        
        return context
    
    def get_initial(self):
        """
        در اینجا مقدار فیلد درخواست دهنده را با توجه به ادرس مقدار دهی میکنیم 
        """
        t = Term.objects.get(is_active=True)
        student = self.kwargs['pk']
        return {'student': student, 'term': t.id}

    # def get_success_url(self):
    #     return reverse('sdg-list')
    


    
