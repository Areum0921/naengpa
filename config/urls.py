"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from naengpa import views
from django.conf.urls import url

from django.contrib.auth.decorators import login_required # 로그인 상태여야한다.
from  django.views.decorators.cache import never_cache

from django.conf.urls.static import static # 정적파일 제공
from django.conf import settings # settings.py에 설정한 미디어 경로 사용

urlpatterns = [
    path('admin/', admin.site.urls),
    path('naengpa/',include('naengpa.urls')),
    path('common/',include('common.urls')),
    path('',views.index, name='index'), # 기본주소
    path('ckeditor/',include('ckeditor_uploader.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)