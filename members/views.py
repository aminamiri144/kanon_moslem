from members.models import *
from .forms import *
from kanon_moslem.aminBaseViews import *
from education_management.models import *

# Create your views here.


class TeacherCreateView(BaseCreateViewAmin):
    model = Teacher
    form_class = TeacherCreateForm
    success_message = 'سرگروه جدید با موفقیت افزوده شد !'
    PAGE_TITLE = 'افزودن سرگروه'
    ACTION_URL = 'teacher-add'
    BUTTON_TITLE = 'افزودن سرگروه'
    date_field_id = 'id_birth_date'


    

class StudentCreateView(BaseCreateViewAmin):
    model = Student
    form_class = StudentCreateForm
    success_message = 'متربی جدید با موفقیت افزوده شد !'
    PAGE_TITLE = 'ثبت نام متربی'
    ACTION_URL = 'student-add'
    BUTTON_TITLE = "ثبت نام متربی"
    date_field_id = 'id_birth_date'
    def get_success_url(self):
        return reverse('student-view')


    


class StudentDetailView(BaseDetailViewAmin):
    PAGE_TITLE = 'مشخصات متربی'
    PAGE_DESCRIPTION = ''
    model = Student
    fields = [
        'first_name',
        'last_name',
        'username',
        'mobile',
        'address',
        'clas',
        'school_name',
        'father_name',
        'mather_name', 
        'register_date',
        'birth_date', 
        'home_phone', 
        'father_phone', 
        'mather_phone', 
    ]
    models_property = ['register_date','birth_date']



# class StudentModelView(ListView):
#     model= Student
#     PAGE_TITLE = "لیست متربیان"
#     PAGE_DESCRIPTION = 'کانون تربیتی حضرت مسلم ابن عقیل'
#     create_button_title = 'افزودن متربی جدید' 
#     create_url = 'student-add' 
#     fields_verbose = ['شناسه', 'نام ونام خانوادگی', 'گروه', 'کدملی', 'تاریخ تولد', 'شماره همراه']
#     fields = ['id', 'get_full_name', 'clas', 'username', 'jd_birth_date', 'mobile'] 


class StudentListView(LoginRequiredMixin, ListView):
    paginate_by = 20
    model = Student
    context_object_name = 'students'
    template_name = 'student/list.html'

    def get_queryset(self):
        value = self.request.GET.get('q', '')
        option = self.request.GET.get('option', '')
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





