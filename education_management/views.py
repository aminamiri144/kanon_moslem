from django.http import HttpResponse
from django.shortcuts import render, redirect
from education_management.models import *
from kanon_moslem.aminBaseViews import *
from kanon_moslem.views import *
from education_management.forms import *
from members.models import *
from django.views.generic.edit import UpdateView


class TermModalCreateView(NoStudent, BaseCreateViewAmin):
    model = Term
    form_class = TermCreateForm
    success_message = 'ترم جدید با موفقیت افزوده شد !'
    PAGE_TITLE = 'افزودن ترم جدید'
    ACTION_URL = 'term-add'
    BUTTON_TITLE = "اضافه کردن ترم"

    def get_success_url(self):
        return reverse('term-view')


class TermModelView(NoStudent, ListViewAmin):
    model = Term
    PAGE_TITLE = "امور آموزشی"
    PAGE_DESCRIPTION = 'مدیریت ترم های تحصیلی'
    create_button_title = 'افزودن ترم تحصیلی'
    create_url = 'term-add'
    fields_verbose = ['شناسه', 'عنوان ترم', 'ترم فعال']
    fields = ['id', 'get_full_title', 'get_is_active']


class LessonModalCreateView(NoStudent, BaseCreateViewAmin):
    model = Lesson
    form_class = LessonCreateForm
    success_message = 'درس جدید با موفقیت افزوده شد !'
    PAGE_TITLE = 'افزودن درس جدید'
    ACTION_URL = 'lesson-add'
    BUTTON_TITLE = "اضافه کردن درس"

    def get_success_url(self):
        return reverse('lesson-view')


class LessonModelView(NoStudent, ListViewAmin):
    model = Lesson
    PAGE_TITLE = "امور آموزشی"
    PAGE_DESCRIPTION = 'مدیریت درس ها'
    create_button_title = 'افزودن درس جدید'
    create_url = 'lesson-add'
    fields_verbose = ['شناسه', 'نام درس', 'نوع درس', 'توضیحات', 'ضریب نمره']
    fields = ['id', 'title', 'lesson_type', 'description', 'ratio']


class StudentDisciplineGradeListView(NoStudent, LoginRequiredMixin, ListView):
    paginate_by = 20
    model = DisciplineGrade
    template_name = 'enzebati/enzebati_list.html'

    def get_queryset(self):
        s = Student.objects.get(pk=self.kwargs['pk'])
        self.students_disciplin_grades = self.model.objects.filter(
            student=s).order_by('-created')
        return self.students_disciplin_grades

    def get_context_data(self, **kwargs):
        context = super(StudentDisciplineGradeListView,
                        self).get_context_data(**kwargs)
        s = Student.objects.get(pk=self.kwargs['pk'])
        context['student_id'] = s.id
        context['student_fullname'] = s.get_full_name()
        context['sdg'] = self.students_disciplin_grades
        context['term'] = self.request.session['term_title']
        return context


class SdgCreateView(NoStudent, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = DisciplineGrade
    template_name = 'enzebati/sdg_add.html'
    form_class = DisciplineGradeCreateForm
    success_message = "مورد انضباطی ثبت شد."

    def get_context_data(self, **kwargs):
        """در اینجا فیلد کاستومر یا درخواست دهنده را طوری تنظیم میکنیم که
        فقط درخواست دهنده ای که میخواهیم براش درخواست ثبت کنیم نمایش داده بشه
        و طوره نباشه که همه درخواست دهنده ها در اپشن های فیلد سلکت نمایش داده بشن
        """
        context = super(SdgCreateView, self).get_context_data(**kwargs)
        context['form'].fields['student'].choices.field.queryset = Student.objects.filter(
            pk=self.kwargs['pk'])
        context['form'].fields['term'].choices.field.queryset = Term.objects.filter(
            is_active=True)
        context['student_id'] = self.kwargs['pk']

        return context

    def get_initial(self):
        """
        در اینجا مقدار فیلد درخواست دهنده را با توجه به ادرس مقدار دهی میکنیم
        """
        t = Term.objects.get(is_active=True)
        student = self.kwargs['pk']
        return {'student': student, 'term': t.id}

    def get_success_url(self):
        i = self.kwargs['pk']
        try:
            i = str(i)
        except:
            pass
        return reverse('sdg-list', kwargs={'pk': i})


class GroupReportCreateView(BaseTemplateViewAmin, LoginRequiredMixin, NoStudent):
    template_name = 'eval/group_report_create.html'
    PAGE_TITLE = 'ثبت گزارش گروه'
    PAGE_DESCRIPTION = ''

    def get_context_data(self, more_data=None, **kwargs):
        context = super(GroupReportCreateView, self).get_context_data(**kwargs)
        self.clas = Class.objects.get(id=self.kwargs['pk'])
        context['class_id'] = self.kwargs['pk']
        context['class_name'] = self.clas.name
        context['students'] = Student.objects.filter(clas=self.clas)
        context['term'] = self.request.session['term_title']
        context['form'] = ReportHalgheForm()
        if more_data is not None:
            for data in more_data:
                context[data['key']] = data['value']
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request, *args, **kwargs):

        form = ReportHalgheForm(request.POST)
        this_term = Term.objects.get(id=self.request.session['term_id'])
        if form.is_valid():
            report_title = request.POST.get('title')
            report_type = request.POST.get('report_type')
            date = request.POST.get('date').replace('/', '-')
            new_report = GroupReport()
            new_report.title = report_title
            new_report.report_type = ReportTypes.objects.get(id=report_type)
            new_report.clas = Class.objects.get(id=self.kwargs['pk'])
            new_report.term = this_term
            new_report.date = date
            new_report.save()
        else:
            return render(request, self.template_name, context=self.get_context_data([{'key': 'form', 'value': form}]))

        students_id = request.POST.getlist('student_id')
        hozor = request.POST.getlist('hozor')
        hozor_description = request.POST.getlist('description1')
        takhir = request.POST.getlist('takhir')
        takhir_description = request.POST.getlist('description2')
        result = list(zip(students_id, hozor, hozor_description,
                          takhir, takhir_description))
        for dg in result:
            # غیبت غیر موجه
            if dg[1] in '0':
                new_dg = DisciplineGrade()
                new_dg.report = new_report
                new_dg.student = Student.objects.get(id=dg[0])
                new_dg.discipline = Discipline.objects.filter(
                    title__contains='غیبت').first()
                new_dg.created = date
                new_dg.grade = -3
                new_dg.term = this_term
                new_dg.description = dg[2]
                new_dg.save()

            # غیبت موجه
            elif dg[1] in '1':
                new_dg = DisciplineGrade()
                new_dg.report = new_report
                new_dg.student = Student.objects.get(id=dg[0])
                new_dg.discipline = Discipline.objects.filter(
                    title__contains='غیبت').first()
                new_dg.created = date
                new_dg.grade = -1
                new_dg.term = this_term
                new_dg.description = dg[2]
                new_dg.save()
            # حاضر
            elif dg[1] == '2':
                # تاخیر غیر موجه
                if dg[3] == '0':
                    new_dgt = DisciplineGrade()
                    new_dgt.report = new_report
                    new_dgt.student = Student.objects.get(id=dg[0])
                    new_dgt.discipline = Discipline.objects.filter(
                        title__contains='تاخیر').first()
                    new_dgt.created = date
                    new_dgt.grade = -2
                    new_dgt.term = this_term
                    new_dgt.description = dg[4]
                    new_dgt.save()
                # تاخیر موجه
                elif dg[3] == '1':
                    new_dgt = DisciplineGrade()
                    new_dgt.report = new_report
                    new_dgt.student = Student.objects.get(id=dg[0])
                    new_dgt.discipline = Discipline.objects.filter(
                        title__contains='تاخیر').first()
                    new_dgt.created = date
                    new_dgt.grade = -1
                    new_dgt.term = this_term
                    new_dgt.description = dg[4]
                    new_dgt.save()
        return redirect(f'/edu/report/detail/{new_report.id}')


class GroupReportDetailView(NoStudent, LoginRequiredMixin, SuccessMessageMixin, BaseDetailViewAmin):
    PAGE_TITLE = 'گزارش گروه'
    PAGE_DESCRIPTION = 'گزارش روزانه حضور غیاب برنامه ها'
    model = GroupReport
    template_name = 'eval/group_report_detail.html'
    fields = ['title', 'report_type', 'clas', 'term', 'date']
    models_property = ['date']

    def get_more_contexts(self):
        sdgs = DisciplineGrade.objects.filter(report__id=self.pk)
        pk = self.kwargs['pk']
        return {'sdgs': sdgs, 'pk': pk}


class GroupReportsListView(NoStudent, LoginRequiredMixin, ListView):
    paginate_by = 20
    model = GroupReport
    template_name = 'eval/group_reports_list.html'

    def get_queryset(self):
        term = Term.objects.get(id=self.request.session['term_id'])

        if hasattr(self.request.user, 'teacher'):
            t_id = self.request.user.id
            teacher = Teacher.objects.get(id=t_id)
            self.t_class = teacher.clss

            self.rgs = GroupReport.objects.filter(
                clas=self.t_class, term=term).order_by('-date')
            return self.rgs
        else:
            self.rgs = GroupReport.objects.filter(term=term).order_by('-date')
            return self.rgs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rsg'] = self.rgs
        try:
            context['title'] = f"گزارش های گروه {self.t_class} "
        except:
            context['title'] = f" گزارش های گروه ها"

        context['description'] = ""
        context['term'] = self.request.session['term_title']

        return context


class GroupReportDeleteView(AminView, LoginRequiredMixin, NoStudent, SuccessMessageMixin):
    template_name = 'eval/group_report_delete.html'
    success_message = "گزارش با موفقیت حذف شد"

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, request, *args, **kwargs):
        report_id = self.kwargs['pk']
        report = GroupReport.objects.get(pk=report_id)
        report.delete()
        return redirect('/')


class SDGListView4Students(LoginRequiredMixin, ListView):
    paginate_by = 20
    model = DisciplineGrade
    template_name = 'spanel/student_enzebati_list.html'

    def get_queryset(self):
        s = Student.objects.get(pk=self.kwargs['pk'])
        term = Term.objects.get(pk=self.request.session['term_id'])
        self.students_disciplin_grades = self.model.objects.filter(
            student=s, term=term).order_by('-created')
        return self.students_disciplin_grades

    def get_context_data(self, **kwargs):
        context = super(SDGListView4Students,
                        self).get_context_data(**kwargs)
        s = Student.objects.get(pk=self.kwargs['pk'])
        context['student_id'] = s.id
        context['student_fullname'] = s.get_full_name()
        context['sdg'] = self.students_disciplin_grades
        context['term'] = self.request.session['term_title']
        return context
