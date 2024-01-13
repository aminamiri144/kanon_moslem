from django.urls import path
from education_management.views import *

urlpatterns = [
    path('term/', TermModelView.as_view(), name='term-view'),
    path('term/add', TermModalCreateView.as_view(), name='term-add'),
    path('lesson/', LessonModelView.as_view(), name='lesson-view'),
    path('lesson/add', LessonModalCreateView.as_view(), name='lesson-add'),
    path('sdg/<int:pk>',StudentDisciplineGradeListView.as_view(), name='sdg-list'),
    path('sdg/add/<int:pk>',SdgCreateView.as_view(), name='sdg-add'),
    
]
