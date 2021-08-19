# 서브앱의 urls.py
# 같은 위치의 view.py 함수로 연결 역할 (path)
# view 식별 못할 시 import

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'naengpa'

router = DefaultRouter()
router.register('Recipe',views.RecipeViewSet)

# 프로젝트 폴더 urls.py 내 urlpatterns 처럼 경로 추가 가능
urlpatterns = [
    path('api/',include(router.urls)),
    path('', views.index, name='index'),
    path('<int:recipe_id>/',views.detail, name='detail'),
    path('review/create/<int:recipe_id>/',views.review_create, name="review_create"),
    path('create/', views.recipe_create, name="recipe_create"),
    path('recipe/modify/<int:recipe_id>/', views.recipe_modify, name="recipe_modify"),
    path('recipe/delete/<int:recipe_id>/', views.recipe_delete, name="recipe_delete"),
]
