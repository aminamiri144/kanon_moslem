from members.models import *
from .forms import *
from kanon_moslem.aminBaseViews import *
from education_management.models import *
from kanon_moslem.views import *

# Create your views here.


class TeacherCreateView(NoStudent, BaseCreateViewAmin):
    model = Teacher
    form_class = TeacherCreateForm
    success_message = 'سرگروه جدید با موفقیت افزوده شد !'
    PAGE_TITLE = 'افزودن سرگروه'
    ACTION_URL = 'teacher-add'
    BUTTON_TITLE = 'افزودن سرگروه'
    DATE_FIELD_ID = 'id_birth_date'
    SUCCESS_URL = 'teacher-detail'

    

class StudentCreateView(NoStudent, BaseCreateViewAmin):
    model = Student
    form_class = StudentCreateForm
    success_message = 'متربی جدید با موفقیت افزوده شد !'
    PAGE_TITLE = 'ثبت نام متربی'
    ACTION_URL = 'student-add'
    BUTTON_TITLE = "ثبت نام متربی"
    DATE_FIELD_ID = 'id_birth_date'
    SUCCESS_URL = 'student-detail'




    


class StudentDetailView(NoStudent, BaseDetailViewAmin):
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




class TeacherDetailView(NoStudent, BaseDetailViewAmin):
    PAGE_TITLE = 'مشخصات سرگروه'
    PAGE_DESCRIPTION = ''
    model = Teacher
    fields = [
        'first_name',
        'last_name',
        'mobile',
        'username',
        'birth_date',  
        'clss',
        'experiences',
        'study_field',  
        'address',
    ]
    models_property = ['birth_date']


class StudentListView(AminView ,NoStudent, LoginRequiredMixin, ListView):
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
            if hasattr(self.request.user, 'teacher'):
                t_id = self.request.user.id
                teacher = Teacher.objects.get(id=t_id)
                tc = teacher.clss
                object_list = self.model.objects.filter(clas_id=tc.id)
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





