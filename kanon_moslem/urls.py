"""kanon_moslem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from kanon_moslem.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PanelView.as_view(), name="panel"),
    path('spanel/', StudentPanelView.as_view(), name="spanel"),
    path('tpanel/', TeacherPanelView.as_view(), name="tpanel"),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('change/term/', ChangeSystemTerm.as_view(), name='change_term'),
    path('m/', include("members.urls")),
    path('edu/', include("education_management.urls")),
    path('eval/', include("evaluation.urls")),
    path('tuition/', include("tuition.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.ASSETS_URL, document_root=settings.ASSETS_ROOT)