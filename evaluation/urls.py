from django.urls import path
from .views import *

urlpatterns = [
    # path('teacher/add', TeacherCreateView.as_view(), name='teacher-add'),
    path('lesson/selection', SelectionLessonClass.as_view(), name='selection-add'),
    path('grade/student/<int:pk>', GradeStudent.as_view(), name='grade-student-add'),
    path('karname/term/<int:pk>', GradesDetailView.as_view(), name='student-term-karname'),
]
