from .forms import LessonClassSelectionForm
from education_management.models import SelectedLesson, ControlSelection
from kanon_moslem.views import *
from kanon_moslem.aminBaseViews import *
from education_management.models import DisciplineGrade


class SelectionLessonClass(View, NoStudent, LoginRequiredMixin):
    form_class = LessonClassSelectionForm
    template_name = "eval/select_lesson_class.html"
    success_message = "انتخاب واحد با موفقیت انجام شد."

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form, "term": self.request.session['term_title']})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            clas = form.cleaned_data['clas']
            lesson = form.cleaned_data['lesson']
            term = Term.objects.filter(id=self.request.session['term_id']).first()

            students = Student.objects.filter(clas=clas, is_active=True)
            try:
                ControlSelection(clas=clas, term=term, lesson=lesson).save()
                for student in students:
                    try:
                        SelectedLesson(student=student,
                                       lesson=lesson, term=term).save()
                    except:
                        pass
            except:
                messages = [{'message': 'این درس قبلا برای این گروه گرفته شده است.', 'tag': 'danger', }]
                return render(request, self.template_name, {"form": form, "messages": messages})

        messages = [{'message': 'انتخاب واحد با موفقیت انجام شد.', 'tag': 'success', }]
        return render(request, self.template_name,
                      {"form": form, "messages": messages, "term": self.request.session['term_title']})


class GradeStudent(NoStudent, View, LoginRequiredMixin):
    template_name = 'eval/student_nomre_term.html'

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(id=self.kwargs['pk'])
        term = Term.objects.filter(id=self.request.session['term_id']).first()

        grades = SelectedLesson.objects.filter(student=student, term=term)

        return render(request, self.template_name,
                      {"grades": grades, 'student': student, 'term': self.request.session['term_title']})

    def post(self, request, *args, **kwargs):
        lesson = request.POST.getlist('lesson')
        grade = request.POST.getlist('grade')
        desc = request.POST.getlist('description')
        result = list(zip(lesson, grade, desc))
        student = Student.objects.get(id=self.kwargs['pk'])
        term = Term.objects.filter(id=self.request.session['term_id']).first()
        for g in result:
            s = SelectedLesson.objects.get(student=student, lesson_id=g[0], term=term)
            s.grade = g[1]
            s.description = g[2]
            s.save()
        grades = SelectedLesson.objects.filter(student=student, term=term)
        messages.add_message(self.request, messages.SUCCESS,
                             f'کارنامه {student.get_full_name()} با موفقیت ثبت و ویرایش شد.')

        return render(request, self.template_name,
                      {"grades": grades, 'student': student, 'term': self.request.session['term_title']})


class GradesDetailView(AminView, LoginRequiredMixin):

    def get_template_names(self):
        if hasattr(self.request.user, 'student'):
            return "spanel/student_karname.html"
        else:
            return "eval/karname.html"

    def get(self, request, *args, **kwargs):
        if hasattr(self.request.user, 'student'):
            student = Student.objects.get(id=self.request.user.id)
        else:
            student = Student.objects.get(id=self.kwargs['pk'])
        term = Term.objects.get(id=self.request.session["term_id"])
        grades = SelectedLesson.objects.filter(student=student, term=term)
        sum_grades = 0
        lesson_count = 0
        for g in grades:
            if g.grade not in ['n', 'g']:
                n = int(g.grade)
                l = g.lesson.ratio
                sum_grades += n * l
                lesson_count += l

        try:
            average = round(sum_grades / lesson_count, 1)
        except:
            average = 8

        if 0 <= average < 1:
            nomre_tosifi = "بسیار ضعیف"
        elif 1 <= average < 2:
            nomre_tosifi = "ضعیف"
        elif 2 <= average < 3:
            nomre_tosifi = "متوسط"
        elif 3 <= average < 4:
            nomre_tosifi = "خوب"
        elif 4 <= average < 5:
            nomre_tosifi = "بسیار خوب"
        else:
            nomre_tosifi = "ثبت نشده"
            average = ''

        context = {
            "grades": grades,
            'student': student,
            'term': term,
            'average': average,
            'nt': nomre_tosifi,
        }

        return render(request, self.get_template_names(), context)


class GroupTermGrades(AminView, LoginRequiredMixin, NoStudent):
    PAGE_TITLE = ''
    PAGE_DESCRIPTION = ''
    template_name = 'eval/group_karname_term.html'

    def get(self, request, *args, **kwargs):
        term = Term.objects.get(id=self.request.session['term_id'])
        if hasattr(self.request.user, 'teacher'):
            t_id = self.request.user.id
            self.t_class = Class.objects.get(teacher__id=t_id)
            lessons_selected_4clas = ControlSelection.objects.filter(clas_id=self.t_class.id, term=term)
            lessons = [l.lesson.title for l in lessons_selected_4clas]
            students_grades = []
            for student in Student.objects.filter(clas_id=self.t_class.id, is_active=True):
                grades = SelectedLesson.objects.filter(student=student, term=term)
                enzebati = DisciplineGrade.objects.filter(student=student, term=term)
                nomre = 20.0
                family_nomre = 20.0
                fogh_nomre = 20.0
                for e in enzebati:
                    try:
                        if 'خانواد' in e.report.report_type.title:
                            family_nomre += float(e.grade)
                        elif 'والدین' in e.report.report_type.title:
                            family_nomre += float(e.grade)
                        elif 'فوق' in e.report.report_type.title:
                            fogh_nomre += float(e.grade)
                        else:
                            nomre += float(e.grade)
                    except:
                        nomre += float(e.grade)
                sg = {
                    'student': student,
                    'grades': grades,
                    'nomre_enzebati': nomre,
                    'nomre_family': family_nomre,
                    'nomre_fogh': fogh_nomre,
                }
                students_grades.append(sg)
            context = {
                'term': self.request.session['term_title'],
                'group_name': self.t_class.name,
                'students_grades': students_grades,
                'lessons': lessons,
            }
            return render(request, self.template_name, context)
        else:
            messages.add_message(self.request, messages.WARNING, 'فقط مربیان به این صفحه دسترسی دارند')
            return redirect('/')

    def post(self, request, *args, **kwargs):
        t_id = self.request.user.id
        t_class = Class.objects.get(teacher__id=t_id)
        term = Term.objects.get(id=self.request.session['term_id'])
        students = Student.objects.filter(clas=t_class, is_active=True)
        for student in students:
            grades = SelectedLesson.objects.filter(student=student, term=term)
            for grade in grades:
                nomre = request.POST.get(f'grade_{grade.id}')
                grade.grade = nomre
                grade.save()

        messages.add_message(self.request, messages.SUCCESS,
                             f'نمرات گروه {t_class.name} با موفقیت ثبت و بروزرسانی شد')
        return redirect('/tpanel')


class GroupTermKarname(AminView, LoginRequiredMixin, NoStudent):
    PAGE_TITLE = ''
    PAGE_DESCRIPTION = ''
    template_name = 'eval/group_karname_term_view.html'

    def get(self, request, *args, **kwargs):
        term = Term.objects.get(id=self.request.session['term_id'])
        if hasattr(self.request.user, 'teacher'):
            t_id = self.request.user.id
            self.t_class = Class.objects.get(teacher__id=t_id)
        elif request.GET.get('pk') is not None:
            self.t_class = Class.objects.get(id=request.GET.get('pk'))
        else:
            messages.add_message(self.request, messages.WARNING, 'این صفحه در دسترس نیست')
            return redirect('/')
        lessons_selected_4clas = ControlSelection.objects.filter(clas_id=self.t_class.id, term=term)
        lessons = [l.lesson.title for l in lessons_selected_4clas]
        students_grades = []
        for student in Student.objects.filter(clas_id=self.t_class.id, is_active=True):
            grades = SelectedLesson.objects.filter(student=student, term=term)
            sum_grades = 0
            lesson_count = 0
            for g in grades:
                if g.grade not in ['n', 'g']:
                    n = int(g.grade)
                    l = g.lesson.ratio
                    sum_grades += n * l
                    lesson_count += l

            try:
                average = round(sum_grades / lesson_count, 1)
            except:
                average = 8

            if 0 <= average < 1:
                nomre_tosifi = "بسیار ضعیف"
            elif 1 <= average < 2:
                nomre_tosifi = "ضعیف"
            elif 2 <= average < 3:
                nomre_tosifi = "متوسط"
            elif 3 <= average < 4:
                nomre_tosifi = "خوب"
            elif 4 <= average < 5:
                nomre_tosifi = "بسیار خوب"
            else:
                nomre_tosifi = "ثبت نشده"
                average = ''

            sg = {
                "grades": grades,
                'student': student,
                'average': average,
                'nt': nomre_tosifi,
            }
            students_grades.append(sg)
        context = {
            'term': self.request.session['term_title'],
            'group_name': self.t_class.name,
            'students_grades': students_grades,
            'lessons': lessons,
        }
        return render(request, self.template_name, context)
