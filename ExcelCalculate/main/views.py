from django.shortcuts import render, redirect
from .models import *
from random import *
from sendEmail.views import *

# Create your views here.
def index(request):
    # 로그인된 사용자만 접근
    # 조건문 : 사용자의 정보가 세션에 존재하면 메인화면으로 출력,
    # 만약, 사용자의 정보가 세션에 없다면 로그인 화면으로 출력
    if 'user_name' in request.session.keys():
        return render(request, "main/index.html") # 사용자의 세션정보가 담긴 상태의 index.html
    else:
        return redirect('main_signin')

    # return render(request, "main/index.html") # 아무런 세션 정보가 없는 index.html

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

def login(request):
    # 로그인된 사용자만 이용할 수 있도록 구현
    # 이 때, 현재 사용자가 로그인된 사용자인지 판단하기 위해 세션사용 FROM (verify 함수에서 만든 세션)
    # 세션 처리 진행함
    # 각각 독립된 객체로 진행됨

    loginEmail = request.POST['loginEmail']
    # html의 name이 loginEmail이라서 사용함
    loginPW = request.POST['loginPW']
    user = User.objects.get(user_email=loginEmail)

    # 회원가입시 입력한 패스워드와 입력한 패스워드가 같은지 확인
    if user.user_password == loginPW:
        request.session['user_name'] = user.user_name # 사용자가 회원가입 시, 입력한 정보
        request.session['user_email'] = user.user_email # 사용자가 회원가입 시, 입력한 정보
        return redirect('main_index')
    
    else:
        # 로그인 실패, 정보가 다름
        return redirect("main_loinFail")

    # return None
    #None으로 표시를 해도 오류 안남, HttpResponse("확인문구")로 해도 됨 상관없음

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
    if 'user_name' in request.session.keys():
        return render(request, 'main/result.html') # 사용자의 세션 정보가 담겨져 있는 상태에서의 index.html
    else:
        return redirect("main_signin")
    

def logout(request):
    # 로그아웃의 개념 : 세션 정보를 삭제하는 것
    # 파이썬에서 객체를 지울 때
    del request.session['user_name']
    del request.session['user_email']

    return redirect('main_signin')