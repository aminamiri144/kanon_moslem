from django.urls import path
from members.views import TeacherCreateView

urlpatterns = [
        path('create', TeacherCreateView.as_view(), name='member-create'),
]
