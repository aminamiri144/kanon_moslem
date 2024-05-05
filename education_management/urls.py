from django.urls import path
from education_management.views import *

urlpatterns = [
    path('term/', TermModelView.as_view(), name='term-view'),
    path('term/add', TermModalCreateView.as_view(), name='term-add'),
    path('lesson/', LessonModelView.as_view(), name='lesson-view'),
    path('lesson/add', LessonModalCreateView.as_view(), name='lesson-add'),
    path('sdg/<int:pk>', StudentDisciplineGradeListView.as_view(), name='sdg-list'),
    path('sdg/student/<int:pk>', SDGListView4Students.as_view(), name='sdg4student-list'),
    path('sdg/add/<int:pk>', SdgCreateView.as_view(), name='sdg-add'),
    path('report/add/<int:pk>', GroupReportCreateView.as_view(), name='rg-add'),
    path('report/detail/<int:pk>', GroupReportDetailView.as_view(), name='rg-detail'),
    path('report/delete/<int:pk>', GroupReportDeleteView.as_view(), name='group_report_delete'),
    path('report/list/', GroupReportsListView.as_view(), name='group_reports_list'),

]
