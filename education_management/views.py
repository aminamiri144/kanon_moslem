from django.views.generic import DeleteView
from django.urls import reverse
from django.shortcuts import redirect
from django.http import JsonResponse

from kanon_moslem.views import *
from education_management.forms import *
from members.models import *
from education_management.models import *
from django.contrib import messages


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
        term = Term.objects.get(id=self.request.session['term_id'])
        s = Student.objects.get(pk=self.kwargs['pk'])
        self.students_disciplin_grades = self.model.objects.filter(
            student=s, term=term).order_by('-created')
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

    def get_template_names(self):
        """اگر درخواست AJAX است، تمپلیت مودال را برگردان"""
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest' or self.request.GET.get('modal') == '1':
            return ['enzebati/sdg_add_modal.html']
        return [self.template_name]

    def get_context_data(self, **kwargs):
        """در اینجا فیلد کاستومر یا درخواست دهنده را طوری تنظیم میکنیم که
        فقط درخواست دهنده ای که میخواهیم براش درخواست ثبت کنیم نمایش داده بشه
        و طوره نباشه که همه درخواست دهنده ها در اپشن های فیلد سلکت نمایش داده بشن
        """
        context = super(SdgCreateView, self).get_context_data(**kwargs)
        context['form'].fields['student'].choices.field.queryset = Student.objects.filter(
            pk=self.kwargs['pk'], is_active=True)
        context['form'].fields['term'].choices.field.queryset = Term.objects.filter(
            is_active=True)
        context['student_id'] = self.kwargs['pk']
        context['term'] = self.request.session['term_title']
        return context

    def get_initial(self):
        """
        در اینجا مقدار فیلد درخواست دهنده را با توجه به ادرس مقدار دهی میکنیم
        """
        t = Term.objects.get(is_active=True)
        student = self.kwargs['pk']
        return {'student': student, 'term': t.id}

    def form_valid(self, form):
        """اگر درخواست AJAX است، JSON response برگردان"""
        response = super().form_valid(form)
        
        # اگر درخواست AJAX است
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': self.success_message})
        
        return response

    def form_invalid(self, form):
        """اگر فرم نامعتبر است و درخواست AJAX است، فرم را با خطاها برگردان"""
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return self.render_to_response(self.get_context_data(form=form))
        return super().form_invalid(form)

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
        context['students'] = Student.objects.filter(clas=self.clas, is_active=True)
        context['term'] = self.request.session['term_title']
        context['form'] = ReportHalgheForm()
        if more_data is not None:
            for data in more_data:
                context[data['key']] = data['value']
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request, *args, **kwargs):
        this_term = Term.objects.get(id=self.request.session['term_id'])
        form = ReportHalgheForm(request.POST)
        
        if not form.is_valid():
            messages.add_message(self.request, messages.WARNING, "خطا، گزارش ثبت نشد! لطفا فیلدهای الزامی را پر کنید.")
            return render(request, self.template_name, context=self.get_context_data([{'key': 'form', 'value': form}]))
        
        # دریافت و پردازش داده‌های فرم
        report_title = form.cleaned_data.get('title')
        report_type_id = form.cleaned_data.get('report_type').id
        date = form.cleaned_data.get('date')
        
        # تبدیل تاریخ به فرمت مورد نیاز
        if isinstance(date, str):
            date = date.replace('/', '-')
        
        # ایجاد گزارش جدید
        try:
            report_type = ReportTypes.objects.get(id=report_type_id)
            clas = Class.objects.get(id=self.kwargs['pk'])
            
            # بررسی تکراری نبودن گزارش
            existing_report = GroupReport.objects.filter(
                clas=clas,
                term=this_term,
                date=date,
                report_type=report_type
            ).first()
            
            if existing_report:
                messages.add_message(
                    self.request, 
                    messages.WARNING, 
                    f'گزارش برای این تاریخ و نوع گزارش قبلاً ثبت شده است.'
                )
                return render(request, self.template_name, context=self.get_context_data([{'key': 'form', 'value': form}]))
            
            new_report = GroupReport.objects.create(
                title=report_title,
                report_type=report_type,
                clas=clas,
                term=this_term,
                date=date
            )
        except Exception as e:
            messages.add_message(self.request, messages.ERROR, f'خطا در ایجاد گزارش: {str(e)}')
            return render(request, self.template_name, context=self.get_context_data([{'key': 'form', 'value': form}]))

        # دریافت داده‌های دانش‌آموزان
        students_id = request.POST.getlist('student_id')
        hozor = request.POST.getlist('hozor')
        hozor_description = request.POST.getlist('description1')
        takhir = request.POST.getlist('takhir')
        takhir_description = request.POST.getlist('description2')
        
        # دریافت Discipline ها یکبار (بهینه‌سازی)
        absence_discipline = Discipline.objects.filter(title__contains='غیبت').first()
        delay_discipline = Discipline.objects.filter(title__contains='تاخیر').first()
        
        if not absence_discipline:
            messages.add_message(self.request, messages.ERROR, 'مورد انضباطی "غیبت" یافت نشد. لطفا ابتدا آن را ایجاد کنید.')
            return render(request, self.template_name, context=self.get_context_data([{'key': 'form', 'value': form}]))
        
        if not delay_discipline:
            messages.add_message(self.request, messages.ERROR, 'مورد انضباطی "تاخیر" یافت نشد. لطفا ابتدا آن را ایجاد کنید.')
            return render(request, self.template_name, context=self.get_context_data([{'key': 'form', 'value': form}]))
        
        # دریافت تمام دانش‌آموزان یکبار (بهینه‌سازی)
        student_ids = [int(sid) for sid in students_id]
        students_dict = {s.id: s for s in Student.objects.filter(id__in=student_ids)}
        
        # ایجاد لیست DisciplineGrade برای bulk_create
        discipline_grades_to_create = []
        
        for idx, student_id in enumerate(students_id):
            try:
                student = students_dict.get(int(student_id))
                if not student:
                    continue
                
                hozor_value = hozor[idx] if idx < len(hozor) else '2'
                hozor_desc = hozor_description[idx] if idx < len(hozor_description) else ''
                takhir_value = takhir[idx] if idx < len(takhir) else '2'
                takhir_desc = takhir_description[idx] if idx < len(takhir_description) else ''
                
                # غیبت غیر موجه
                if hozor_value == '0':
                    discipline_grades_to_create.append(
                        DisciplineGrade(
                            report=new_report,
                            student=student,
                            discipline=absence_discipline,
                            created=date,
                            grade=report_type.grade2,
                            term=this_term,
                            description=hozor_desc or None
                        )
                    )
                
                # غیبت موجه
                elif hozor_value == '1':
                    discipline_grades_to_create.append(
                        DisciplineGrade(
                            report=new_report,
                            student=student,
                            discipline=absence_discipline,
                            created=date,
                            grade=report_type.grade1,
                            term=this_term,
                            description=hozor_desc or None
                        )
                    )
                
                # حاضر - بررسی تاخیر
                elif hozor_value == '2':
                    # تاخیر غیر موجه
                    if takhir_value == '0':
                        discipline_grades_to_create.append(
                            DisciplineGrade(
                                report=new_report,
                                student=student,
                                discipline=delay_discipline,
                                created=date,
                                grade=report_type.grade4,
                                term=this_term,
                                description=takhir_desc or None
                            )
                        )
                    # تاخیر موجه
                    elif takhir_value == '1':
                        discipline_grades_to_create.append(
                            DisciplineGrade(
                                report=new_report,
                                student=student,
                                discipline=delay_discipline,
                                created=date,
                                grade=report_type.grade3,
                                term=this_term,
                                description=takhir_desc or None
                            )
                        )
            except (ValueError, IndexError) as e:
                continue
        
        # استفاده از bulk_create برای بهینه‌سازی
        if discipline_grades_to_create:
            DisciplineGrade.objects.bulk_create(discipline_grades_to_create)
        
        messages.add_message(self.request, messages.SUCCESS, f'گزارش با موفقیت ثبت شد. {len(discipline_grades_to_create)} مورد انضباطی ثبت شد.')
        return redirect(reverse('rg-detail', kwargs={'pk': new_report.id}))


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
        
        # محاسبه آمار
        absence_count = 0
        delay_count = 0
        
        for sdg in sdgs:
            if 'غیبت' in sdg.discipline.title:
                absence_count += 1
            elif 'تاخیر' in sdg.discipline.title:
                delay_count += 1
        
        return {
            'sdgs': sdgs, 
            'pk': pk,
            'absence_count': absence_count,
            'delay_count': delay_count,
            'total_count': sdgs.count()
        }


class GroupReportsListView(NoStudent, LoginRequiredMixin, ListView):
    paginate_by = 20
    model = GroupReport
    template_name = 'eval/group_reports_list.html'

    def get_paginate_by(self, queryset):
        per_page = self.request.GET.get('per_page')
        return int(per_page) if per_page and per_page.isdigit() else 10  # مقدار پیش‌فرض ۱۰

    def get_queryset(self):
        term_id = self.request.session.get('term_id')
        term = get_object_or_404(Term, id=term_id)

        value = self.request.GET.get('q', '')
        option = self.request.GET.get('option', '')
        query = {f'{option}__icontains': value}


        if hasattr(self.request.user, 'teacher'):
            self.teacher = get_object_or_404(Teacher, id=self.request.user.id)
            self.rgs = GroupReport.objects.filter(clas=self.teacher.clss, term=term).order_by('-date')
            return self.rgs
        if value:
            self.rgs = GroupReport.objects.filter(**query, term=term).order_by('-date')
        else:
            self.rgs = GroupReport.objects.filter(term=term).order_by('-date')
        return self.rgs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rsg'] = self.rgs
        try:
            context['title'] = f"گزارش های گروه {self.teacher.clss} "
        except:
            context['title'] = f" گزارش های گروه ها"

        context['description'] = ""
        context['term'] = self.request.session['term_title']
        if hasattr(self.request.user, 'teacher'):
            context['clas_id'] = self.teacher.clss.id

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
        messages.add_message(self.request, messages.SUCCESS, 'گزارش با موفقیت حذف شد')
        return redirect(reverse('group_reports_list'))


class GroupReportUpdateView(UpdateView, NoStudent, LoginRequiredMixin):
    model = GroupReport
    form_class = ReportHalgheForm
    template_name = 'eval/group_report_update.html'

    def form_valid(self, form):
        report = self.get_object()
        old_report_type = report.report_type
        old_date = report.date
        
        # ذخیره تغییرات
        response = super().form_valid(form)
        
        # دریافت گزارش به‌روز شده
        updated_report = GroupReport.objects.get(pk=self.kwargs['pk'])
        new_report_type = updated_report.report_type
        new_date = form.cleaned_data.get('date')
        
        # دریافت تمام موارد انضباطی این گزارش
        sdgs = DisciplineGrade.objects.filter(report__id=self.kwargs['pk'])
        
        # اگر نوع گزارش تغییر کرده، نمرات را به‌روزرسانی کن
        if old_report_type.id != new_report_type.id:
            # دریافت Discipline ها
            absence_discipline = Discipline.objects.filter(title__contains='غیبت').first()
            delay_discipline = Discipline.objects.filter(title__contains='تاخیر').first()
            
            updated_count = 0
            for sdg in sdgs:
                updated = False
                
                # اگر غیبت است
                if absence_discipline and sdg.discipline.id == absence_discipline.id:
                    # بررسی اینکه موجه است یا غیرموجه (بر اساس نمره قبلی)
                    if abs(sdg.grade - old_report_type.grade1) < 0.01:  # استفاده از tolerance برای مقایسه float
                        # غیبت موجه بود - نمره جدید را از نوع گزارش جدید بگیر
                        sdg.grade = new_report_type.grade1
                        updated = True
                    elif abs(sdg.grade - old_report_type.grade2) < 0.01:
                        # غیبت غیرموجه بود - نمره جدید را از نوع گزارش جدید بگیر
                        sdg.grade = new_report_type.grade2
                        updated = True
                
                # اگر تاخیر است
                elif delay_discipline and sdg.discipline.id == delay_discipline.id:
                    # بررسی اینکه موجه است یا غیرموجه (بر اساس نمره قبلی)
                    if abs(sdg.grade - old_report_type.grade3) < 0.01:
                        # تاخیر موجه بود - نمره جدید را از نوع گزارش جدید بگیر
                        sdg.grade = new_report_type.grade3
                        updated = True
                    elif abs(sdg.grade - old_report_type.grade4) < 0.01:
                        # تاخیر غیرموجه بود - نمره جدید را از نوع گزارش جدید بگیر
                        sdg.grade = new_report_type.grade4
                        updated = True
                
                if updated:
                    sdg.save()
                    updated_count += 1
            
            if updated_count > 0:
                messages.add_message(
                    self.request, 
                    messages.SUCCESS, 
                    f"سربرگ گزارش گروه با موفقیت ویرایش شد. نمرات {updated_count} مورد انضباطی به‌روزرسانی شد."
                )
            else:
                messages.add_message(
                    self.request, 
                    messages.SUCCESS, 
                    "سربرگ گزارش گروه با موفقیت ویرایش شد."
                )
        
        # به‌روزرسانی تاریخ (اگر تغییر کرده)
        if new_date and new_date != old_date:
            for s in sdgs:
                s.created = new_date
                s.save()
        
        return response

    def get_success_url(self):
        return reverse('rg-detail', kwargs={'pk': self.kwargs['pk']})

    def get_initial(self):
        regdate = GroupReport.objects.get(pk=self.kwargs['pk']).jd_date
        return {'date': regdate}


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


class SDGUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DisciplineGrade
    form_class = DisciplineGradeUpdateForm
    template_name = 'enzebati/sdg_update.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "مورد انضباطی با موفقیت ویرایش شد")
        try:
            id_report = DisciplineGrade.objects.get(pk=self.kwargs['pk']).report.id
            return reverse('rg-detail', kwargs={'pk': id_report})
        except:
            id_report = DisciplineGrade.objects.get(pk=self.kwargs['pk']).student.id
            return reverse('sdg-list', kwargs={'pk': id_report})

    def get_initial(self):
        regdate = DisciplineGrade.objects.get(pk=self.kwargs['pk']).jd_created_date
        return {'created': regdate}


class SDGDeleteView(AminView, LoginRequiredMixin, NoStudent):
    template_name = 'enzebati/sdg_delete.html'

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, request, *args, **kwargs):
        mored_enzebati_id = self.kwargs['pk']
        me = DisciplineGrade.objects.get(pk=mored_enzebati_id)
        me.delete()
        messages.add_message(self.request, messages.SUCCESS, 'مورد انضباطی با موفقیت حذف شد')
        next_url = self.request.POST.get('next')
        print(next_url)
        if next_url:
            return redirect(next_url)
        return redirect('/')
