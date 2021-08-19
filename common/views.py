from django.contrib.auth import authenticate,login
from django.shortcuts import render, redirect
from .forms import UserForm

from django.core.mail.message import EmailMessage
from django.contrib.auth.models import User
from .tokens import account_activation_token
from .email_text import message
from config.key import EMAIL,KEY # key.py에 입력한 값들

from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text

def signup(request):
    """계정생성"""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active=False
            user.save()
            # 비밀번호 8자리이상
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            check = authenticate(username=username, password=raw_password)  # 검증
            #login(request,check) 회원가입 후 바로 로그인

            current_site = get_current_site(request) # 현재 site 객체 얻기
            domain = current_site.domain # 현재 사이트의 도메인
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            # force_bytes로 자연수 user.pk를 bytes로 변환 후, urlsafe_base64_encode로 인코딩
            token = account_activation_token.make_token(user) # 토큰 생성
            message_data = message(domain,uidb64,token) # 보낼 메세지 내용

            mail_title = "인증을 완료해주세요"
            mail_to = user.email # 회원가입시 입력한 이메일주소
            email = EmailMessage(mail_title,message_data,to=[mail_to])
            email.send() # 메세지 발송
            return render(request,'common/signup_mail_check_plz.html')
    else:
        form = UserForm()
    context = {'form':form}
    return render(request, 'common/signup.html', context)


def activate(request, uidb64, token): # 링크 누르면 계정 활성화
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(EMAIL['REDIRECT_PAGE'])
    else:
        return HttpResponse('비정상적인 접근입니다.')

    return



