from django.shortcuts import render

# Create your views here.

from .models import Recipe, Review
from rest_framework import viewsets
from .serializers import RecipeSerializer
from django.shortcuts import render, get_object_or_404,redirect,resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Avg, Func, Q
from django.core.paginator import Paginator
# Func 커스텀 db 함수 만들기용
from .forms import RecipeForm, ReviewForm

# Create your views here.

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class Round(Func): # Avg 함수 값 결과를 소수점 1자리까지만 출력
    function = 'ROUND' # sql round 함수
    template='%(function)s(%(expressions)s, 1)'
    # 질의할 query를 만드는 템플릿, 기본값 : '%(function)s(%(expressions)s)'

def index(request):
    page = request.GET.get('page','1') # 페이지
    kw = request.GET.get('kw','')
    sr = request.GET.get('sr','name') # 검색 기본필터 요리이름

    recipe_list = Recipe.objects.all().order_by('-create_date')\
        .annotate(reviews_count = Count('review'))\
        .annotate(score_avg=Round(Avg('review__score')))

    if kw:

        if sr=='need_ingredient': # 재료로 검색하기
            sp_kw = kw.split(",")  # 검색할 재료 입력 재료구분은 공백없이 ,로 입력받기.
            query = Q()
            for i in recipe_list: # 레시피 리스트들
                ingre_check = False # 재료 여부 체크
                print("재료 여부 초기화",ingre_check)
                sp_ingre = i.need_ingredient.split(",") # 해당 레시피 재료 ,기준으로 쪼개기
                print("?asasdas",sp_kw,sp_ingre)
                if len(sp_ingre)<=len(sp_kw):
                    for j in sp_ingre:
                        if j not in sp_kw:
                            #print("없는재료 발견",j,sp_kw)
                            ingre_check = True
                            break
                #print("checcccck",ingre_check,i)
            #print("결과 쿼리",query)
                    if ingre_check==False: # 없는재료가 없는경우 해당 레시피 id에 해당하는 쿼리 합치기
                        query = query | Q(id=i.id)
                        print("요리가능한 레시피 넘버 " ,i.id)
            print("결과쿼리",query)
            recipe_list = recipe_list.filter(query) # 출력
            #recipe_list = recipe_list.filter(Q(need_ingredient__icontains=kw)).distinct()
        else: # 요리 이름으로 검색
            recipe_list = recipe_list.filter(Q(name__icontains=kw))

    print(kw)
    print(recipe_list)
    selected_cate = request.POST.getlist('category[]')
    print(selected_cate)
    if selected_cate:
        print(selected_cate)
        query = Q()
        for i in selected_cate:
            print(i)
            query = query | Q(category__icontains=i)
            print(query)
        recipe_list = recipe_list.filter(query)
    else:
        print("선택된 카테고리 없음")

    for i in recipe_list:
        ingre = i.need_ingredient # 만들어진 쿼리들의 각 재료들 리스트로 가져오기
        print(ingre.split(","))

    paginator = Paginator(recipe_list,5) # 1페이지당 5개
    page_obj = paginator.get_page(page)

    context = {'recipe_list': page_obj, 'category': selected_cate, 'page': page, 'sr':sr}

    return render(request,'naengpa/recipe_list.html',context)

def detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    context = {'recipe' : recipe}
    return render(request,'naengpa/recipe_detail.html',context)

@login_required(login_url='common:login')
def review_create(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.writer = request.user
            review.create_date = timezone.now()
            review.recipe = recipe
            review.save()
            return redirect('{}#review_{}'.format(resolve_url('naengpa:detail', recipe_id=recipe.id), review.id))
            #return redirect('naengpa:detail', recipe_id=recipe.id)
    #review = Review(recipe=recipe, content=request.POST.get('content'), create_date=timezone.now(),score=request.POST.get('score'))
    else:
        form = ReviewForm()
    context = {'recipe':recipe, 'form':form}
    return render(request, 'naengpa/recipe_detail.html',context)

@login_required(login_url='common:login')
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        # 이미지 등 파일 업로드시에는 request.FILES 추가 해야함!!
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.writer = request.user
            recipe.create_date = timezone.now()
            recipe.save()
            return redirect('naengpa:index')
    else: # 레시피 등록하기 GET방식 <a href=>링크 통한 요청은 GET
        form = RecipeForm()
    context = {'form':form}
    return render(request,'naengpa/recipe_create_form.html', context)

@login_required(login_url='common:login')
def recipe_modify(request, recipe_id): # 레시피 수정
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    print("rrreeecvcc",recipe, recipe_id)
    if request.user != recipe.writer:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('naengpa:detail',recipe_id = recipe.id)

    if request.method == "POST": # 수정완료 버튼
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.modify_date = timezone.now()
            recipe.save()
            return redirect('naengpa:detail', recipe_id = recipe.id) # 수정완료시 해당 글 detail로

    else: # method == GET
        form = RecipeForm(instance=recipe) # 해당글의 원래 정보도 같이 불러온다.

    context = {'form': form}
    return render(request, 'naengpa/recipe_create_form.html',context)

@login_required(login_url='common:login')
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user != recipe.writer:
        messages(request, "삭제권한 없음")
        return redirect('naengpa:detail', recipe_id = recipe.id) # 원래 글로 돌아오기
    recipe.delete()
    return redirect('naengpa:index') # 삭제시 메인 화면으로
