from django.shortcuts import render

# Create your views here.

from .models import Recipe, Review
from rest_framework import viewsets
from .serializers import RecipeSerializer
from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from django.db.models import Count, Avg
from .forms import RecipeForm

# Create your views here.

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

def index(request):
    recipe_list = Recipe.objects.all().order_by('-create_date')\
        .annotate(reviews_count = Count('review'))\
        .annotate(score_avg=Avg('review__score'))
    context = {'recipe_list' : recipe_list}
    return render(request,'naengpa/recipe_list.html',context)

def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {'recipe' : recipe}
    return render(request,'naengpa/recipe_detail.html',context)

def review_create(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    review = Review(recipe=recipe, content=request.POST.get('content'), create_date=timezone.now(),score=request.POST.get('score'))
    review.save()
    return redirect('naengpa:detail',recipe_id=recipe.id)

def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        # 이미지 등 파일 업로드시에는 request.FILES 추가 해야함!!
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.create_date = timezone.now()
            recipe.save()
            return redirect('naengpa:index')
    else: # 레시피 등록하기 GET방식 <a href=>링크 통한 요청은 GET
        form = RecipeForm()
    context = {'form':form}
    return render(request,'naengpa/recipe_create_form.html', context)