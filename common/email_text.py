def message(domain, uidb64, token):
    return f"다음 링크를 클릭해야 회원가입 인증이 완료됩니다. " \
           f"http://{domain}/common/activate/{uidb64}/{token}"