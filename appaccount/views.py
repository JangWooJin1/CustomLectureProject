from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from appaccount.forms import UserForm
from django.db import connection
from django.urls import reverse
from django.views import View

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['user_id']
            password = form.cleaned_data['user_pw']
            query = "INSERT INTO appaccount_user (user_id, user_pw) VALUES (%s, %s)"
            with connection.cursor() as cursor:
                cursor.execute(query, [id, password])
            return redirect('../../search')  # 데이터 저장 성공 시 이동할 URL
    else:
        form = UserForm()
    return render(request, 'account/signup.html', {'form': form})


class LoginView(View):
    template_name = 'account/login.html'

    def get(self, request):
        # GET 요청 처리
        return render(request, self.template_name)

    def post(self, request):
        # POST 요청 처리
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(user_id=username, user_pw=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            # 로그인이 성공했을 때
            request.session['user_id'] = user.user_id  # 사용자 ID를 세션에 저장
            return redirect('search:search')  # /search로 리디렉션
        else:
            # 로그인 실패
            # 여기에서 로그인 실패 메시지를 처리하거나 다른 로직을 추가할 수 있습니다.
            pass
        return render(request, self.template_name)