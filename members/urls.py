from django.urls import path
from members.views import *

urlpatterns = [
    path('teacher/add', TeacherCreateView.as_view(), name='teacher-add'),
    path('teacher/<int:pk>', TeacherDetailView.as_view(), name='teacher-detail'),
    path('student/add', StudentCreateView.as_view(), name='student-add'),
    path('student/update/<int:pk>', StudentUpdateView.as_view(), name='student-update'),
    path('student/', StudentListView.as_view(), name='student-view'),
    path('student/<int:pk>', StudentDetailView.as_view(), name='student-detail'),

]
