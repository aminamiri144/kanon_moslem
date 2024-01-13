from django.urls import path
from members.views import *

urlpatterns = [
    path('teacher/add', TeacherCreateView.as_view(), name='teacher-add'),
    path('student/add', StudentCreateView.as_view(), name='student-add'),
    path('student/<int:pk>',StudentDetailView.as_view(), name='student-detail'),
    path('student/',StudentListView.as_view(), name='student-view'),

]
