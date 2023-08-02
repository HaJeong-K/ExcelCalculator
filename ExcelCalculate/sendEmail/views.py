from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

# Create your views here.
def send(receiverEmail, verifyCode):
    # main > join 함수 내부에서 사용됨
    # receiverEmail : 사용자가 회원가입할 때 입력한 이메일주소
    # verifyCode : 인증코드
    # 인증코드 발송은 에러가 날 가능성이 존재
    # try-except 구문 사용 : Google 이용 >> 개발자가 통제 불가능
    print(receiverEmail, verifyCode)
    try:
        content = {'verifyCode' : verifyCode}
        msg_html = render_to_string("sendEmail/email_format.html", content)
        msg = EmailMessage(subject="[멀티캠퍼스] 인증 코드 발송 메일",
                           body=msg_html,
                           from_email="infoker12@naver.com",
                           bcc=[receiverEmail])
        msg.content_subtype="html"
        msg.send()

        print("sendEmail > views.py > send 함수 임무 완료--------------------")
        return True
    except:
        print("sendEmail > views.py > send 함수 임무 실패--------------------")
        return False
