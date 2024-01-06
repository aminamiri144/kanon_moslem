from django.urls import path
from members.views import *

urlpatterns = [
        path('teacher/add', TeacherCreateView.as_view(), name='teacher-add'),
        path('student/add', StudentCreateView.as_view(), name='student-add'),
]
