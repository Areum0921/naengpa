from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm): # UserCreationForm 상속해서 email 속성 추가
    email = forms.EmailField(label="이메일 주소")

    class Meta:
        model = User
        # 앞 3개 속성은 UserCreationForm이 기본적으로 지닌 속성
        # 사용자이름, 비밀번호1, 비밀번호2 --> 비밀번호 2개가 같은지 규칙검사
        fields = ("username","password1","password2","email")

