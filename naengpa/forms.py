from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['thumbnail','name','category','time','difficulty','need_ingredient','content']

        labels = {
            'thumbnail' : '썸네일 사진 ',
            'name' : '요리이름 ',
            'category' : '카테고리',
            'time' : '조리시간 ',
            'difficulty' : '난이도 ',
            'need_ingredient' : '재료 ',
            'content' : '요리방법 ',
        }

