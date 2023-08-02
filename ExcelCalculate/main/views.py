from django.shortcuts import render, redirect
from .models import *
from random import *
from sendEmail.views import *

# Create your views here.
def index(request):
    return render(request, "main/index.html")

def signup(request):
    return render(request, "main/signup.html")

def join(request):
    print("테스트", request)

    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']
    user = User(user_name = name, user_email = email, user_password = pw)
    user.save()

    print("사용자 정보 저장 완료됨!!")

    # 인증코드 하나 생성
    code = randint(1000, 9000)
    print("인증코드 생성--------------------", code) # 서버가 보낸 코드, 쿠키와 세션

    response = redirect("main_verifyCode") # 응답을 객체로 저장한다
    response.set_cookie('code', code) # 인증코드
    response.set_cookie('user_id', user.id)

    print("응답 객체 완성--------------------", response)

    # 이메일 발송하는 함수 만들어보기
    # 이메일 주소 2개 준비하기
    send_result = send(email, code)
    if send_result:
        print("Main > views.py > 이메일 발송 중...")
        return response
    else:
        return HttpResponse("이메일 발송 실패")



def signin(request):
    return render(request, "main/signin.html")

def verifyCode(request):
    return render(request, "main/verifyCode.html")

def verify(request):
    # 사용자가 입력한 code값을 받아야 함
    user_code = request.POST['verifyCode']

    # 쿠키에 저장된 code값과 매칭시킴 (join 함수 확인)
    cookie_code = request.COOKIES.get('code')
    print("코드 확인: ", user_code, cookie_code)

    if user_code == cookie_code:
        user = User.objects.get(id=request.COOKIES.get('user_id')) #SELECT FROM WHERE id = cookie_id 데이터를 가져오는 것.
        user.user_validate = 1 # True=1 / False=0
        user.save()
    
        print("DB에 user_validate 업데이트---------------------")

        response = redirect('main_index')
        # 저장되어 있는 쿠키 삭제
        response.delete_cookie('code')
        response.delete_cookie('user_id')
        # response.set_cookie('user',user)

        # 사용자 정보를 세션에 저장
        request.session['user_name'] = user.user_name # 로그인 화면 구현
        request.session['user_name'] = user.user_email # 로그인 화면 구현
        return response


    else :
        print("False")
        return redirect("main_verifyCode") # verifyCode 화면으로 돌림
    

    # return redirect("main_index") # 인증이 완료되면 메인화면으로 보내라

def result(request):
    return render(request, "main/result.html")