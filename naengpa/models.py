from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.

class Recipe(models.Model):
    thumbnail = ProcessedImageField(
        upload_to='', # 기본설정해놓은 media 폴더에 저장
        processors=[ResizeToFill(100,100)], # 처리작업 이미지 100,100으로 리사이징
        format='JPEG', # 저장 포맷
        options= {'quality': 90}, # 압축률 설정
        null=False,
        blank=False,
        default=''
    )
    name = models.CharField(max_length=200) # 음식 이름
    time = models.IntegerField() # 조리 시간
    difficulty = models.IntegerField()  # 난이도
    need_ingredient = models.CharField(max_length=200)
    content = models.TextField(default='')
    create_date = models.DateTimeField() # 등록일시

    def __str__(self): # .objects.all() 조회시 id대신 name으로
        return self.name



class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    score = models.IntegerField(null=False, validators=[MaxValueValidator(5),MinValueValidator(1)])

