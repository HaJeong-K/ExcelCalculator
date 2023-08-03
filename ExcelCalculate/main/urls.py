from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="main_index"), 
    path('signup', views.signup, name="main_signup"),
    path('signup/join', views.join, name="main_join"),
    path('signin/login', views.login, name="main_login"),
    path('loginFail', views.loginFail, name="main_loginFail"), 
    path('signin', views.signin, name="main_signin"),
    path('verifyCode', views.verifyCode, name="main_verifyCode"),
    path('verify', views.verify, name="main_verify"), 
    path('result', views.result, name="main_result"),
    path('logout', views.logout, name="main_logout"),
]
    # path('html 함수', views로 연결함, name='views와 연결된 부분을 이름지정')