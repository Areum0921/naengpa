from django import forms
from .models import Recipe, Review
from ckeditor_uploader.fields import RichTextUploadingField


class RecipeForm(forms.ModelForm):
    content = RichTextUploadingField()
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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content','score']
        labels = {
            'content' : '평가내용',
            'score' : '평점'
        }

