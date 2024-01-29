from django.shortcuts import render
from django.views import View
from .forms import LessonClassSelectionForm
from members.models import Student
from education_management.models import SelectedLesson, Term, ControlSelection
from kanon_moslem.views import *
from kanon_moslem.aminBaseViews import *
# Create your views here.


class SelectionLessonClass(NoStudent, View, LoginRequiredMixin):
    form_class = LessonClassSelectionForm
    template_name = "eval/select_lesson_class.html"
    success_message = "انتخاب واحد با موفقیت انجام شد."

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            clas = form.cleaned_data['clas']
            lesson = form.cleaned_data['lesson']
            term = Term.objects.filter(is_active=True).first()

            students = Student.objects.filter(clas=clas)
            try:
                ControlSelection(clas=clas, term=term, lesson=lesson).save()
                for student in students:
                    SelectedLesson(student=student,
                                   lesson=lesson, term=term).save()
            except:
                messages = [
                    {'message': 'این درس قبلا برای این گروه گرفته شده است.', 'tag': 'danger', }]
                return render(request, self.template_name, {"form": form, "messages": messages})

        messages = [
            {'message': 'انتخاب واحد با موفقیت انجام شد.', 'tag': 'success', }]
        return render(request, self.template_name, {"form": form, "messages": messages})


class GradeStudent(NoStudent, View, LoginRequiredMixin):
    template_name = 'eval/student_nomre_term.html'

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(id=self.kwargs['pk'])
        term = Term.objects.filter(is_active=True).first()

        grades = SelectedLesson.objects.filter(student=student, term=term)

        return render(request, self.template_name, {"grades": grades, 'student': student})

    def post(self, request, *args, **kwargs):
        lesson = request.POST.getlist('lesson')
        grade = request.POST.getlist('grade')
        result = list(zip(lesson, grade))
        student = Student.objects.get(id=self.kwargs['pk'])

        for g in result:
            s = SelectedLesson.objects.get(student=student, lesson_id=g[0])
            s.grade = g[1]
            s.save()
        term = Term.objects.filter(is_active=True).first()
        grades = SelectedLesson.objects.filter(student=student, term=term)

        messages = [
            {'message': ' نمرات با موفقیت ثبت و بروزرسانی شد.', 'tag': 'success', }]

        return render(request, self.template_name, {"grades": grades, 'student': student, "messages": messages})


class GradesDetailView(View, LoginRequiredMixin):
    


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
        term = Term.objects.filter(is_active=True).first()
        grades = SelectedLesson.objects.filter(student=student, term=term)
        sum_grades = 0
        lesson_count = 0
        for g in grades:
            if g.grade not in ['n', 'g']:
                n = int(g.grade)
                l = g.lesson.ratio
                sum_grades += n * l
                lesson_count += l

        average = round(sum_grades / lesson_count, 1)
        nomre_tosifi = ""
        if  0 <= average < 1 :
            nomre_tosifi = "بسیار ضعیف"
        elif 1 <= average < 2 :
            nomre_tosifi = "ضعیف"
        elif 2 <= average < 3 :
            nomre_tosifi = "متوسط"
        elif 3 <= average < 4 :
            nomre_tosifi = "خوب"
        elif 4 <= average < 5 :
            nomre_tosifi = "بسیار خوب"
        else:
            nomre_tosifi = "نامشخص"
        

        context = {
            "grades": grades,
            'student': student,
            'term': term,
            'average':  average,
            'nt': nomre_tosifi,
        }

        return render(request, self.get_template_names(), context)
