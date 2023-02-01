from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path("uploadImage", views.upload_image, name="upload_image"),
    path("register", views.register, name="register"),
    path("sendEmailCode", views.send_email_code, name="send_email_code"),
    path("login", views.login, name="login"),
    path("verifyToken", views.verify_token, name="verify_token"),
    path("modifyPassword", views.modify_password, name="modify_password"),
]
