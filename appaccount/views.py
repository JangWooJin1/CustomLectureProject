from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from appaccount.forms import UserForm
from django.db import connection
from .models import User

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            query = "INSERT INTO appaccount_user (user_id, password) VALUES (%s, %s)"
            with connection.cursor() as cursor:
                cursor.execute(query, [id, password])
            return redirect('../../search')  # 데이터 저장 성공 시 이동할 URL
    else:
        form = UserForm()
    return render(request, 'appaccount/signup.html', {'form': form})