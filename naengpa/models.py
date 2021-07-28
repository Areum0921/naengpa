from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.

class Recipe(models.Model):
    # 썸네일용 원본파일 리사이징해서 thumbnail폴더에 저장
    thumbnail = ProcessedImageField(
        upload_to='',
        processors=[ResizeToFill(400,300)], # 처리작업 이미지 100,100으로 리사이징
        format='JPEG', # 저장 포맷
        options= {'quality': 80}, # 압축률 설정
        null=False,
        blank=False,
        default='',
    )

    name = models.CharField(max_length=200) # 음식 이름
    time = models.IntegerField() # 조리 시간
    difficulty = models.IntegerField()  # 난이도
    need_ingredient = models.CharField(max_length=200)
    content = models.TextField(default='')
    create_date = models.DateTimeField() # 등록일시
    category = models.CharField(max_length=10, default='', null=False, blank=False) # 한식, 양식, 중식, 일식
    def __str__(self): # .objects.all() 조회시 id대신 name으로
        return self.name



class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    score = models.IntegerField(null=False, validators=[MaxValueValidator(5),MinValueValidator(1)])

