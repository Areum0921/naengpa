# 서브앱의 urls.py
# 같은 위치의 view.py 함수로 연결 역할 (path)
# view 식별 못할 시 import

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf.urls.static import static # 정적파일 제공
from django.conf import settings # settings.py에 설정한 미디어 경로 사용

app_name = 'naengpa'

router = DefaultRouter()
router.register('Recipe',views.RecipeViewSet)

# 프로젝트 폴더 urls.py 내 urlpatterns 처럼 경로 추가 가능
urlpatterns = [
    path('api/',include(router.urls)),
    path('naengpa/', views.index, name='index'),
    path('naengpa/<int:recipe_id>/',views.detail, name='detail'),
    path('review/create/<int:recipe_id>/',views.review_create, name="review_create"),
    path('naengpa/create/', views.recipe_create, name="recipe_create")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)