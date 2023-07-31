from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def signup(request):
    return render(request, "main/signup.html")

def join(request):
    print(request)

    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    user = User(user_name = name, user_email = email, user_password = pw)
    user.save()

    print("사용자 정보 저장 완료됨!!")

    return redirect("main_verifyCode")

def signin(request):
    return render(request, "main/signin.html")

def verifyCode(request):
    return render(request, "main/verifyCode.html")

def verify(request):
    return redirect("main_index") # 인증이 완료되면 메인화면으로 보내라

def result(request):
    return render(request, "main/result.html")