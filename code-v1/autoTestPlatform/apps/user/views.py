import json
import logging
import os

from addict import Dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Image, Register
from .sendMail import Sender
from .token import Token
from .auth_token import AuthToken, generator

logger = logging.getLogger("user")
BASE_DIR = os.path.dirname(__file__)


# Create your views here.


def __jsoner(resp_data):
    return HttpResponse(
        json.dumps(resp_data),
        content_type="application/json; charset=utf-8",
        status=200,
    )


@csrf_exempt
def upload_image(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            image = request.FILES.get("headPortrait", None)
            logger.debug("image name: {}".format(str(image.name)))
            import uuid

            filename = str(uuid.uuid1()) + os.path.splitext(image.name)[1]
            savename = os.path.join(
                os.path.dirname(__file__), "uploadImage/{}".format(filename)
            ).replace("\\", "/")
            if image:
                with open(savename, "wb") as file:
                    file.write(image.read())
            else:
                raise Exception("save image FAILURE...")
            image_data = {"image_path": savename.replace("\\", "/")}
            resp_data.update(image_data)
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            logger.error(str(e))
            resp_data.desc = "FAILURE"
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def register(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            uuid = post_data.uuid
            if uuid in [{}, None, ""]:
                raise Exception("UUID ERROR...")
            logger.debug("image name: {}".format(post_data.image_name))
            if len(post_data.image_name):
                image_data = {
                    "uuid": uuid,
                    "image_path": post_data.image_path or None,
                    "image_name": post_data.image_name or None,
                    "image_size": post_data.image_size or None,
                }
                Image.objects.create(**image_data)
                logger.debug("db create SUCCESS...")
                resp_data.image_data = image_data
            user_data = {
                "uuid": uuid,
                "username": post_data.username,
                "password": post_data.password,
                "gender": post_data.gender,
                "email": post_data.email,
                "fronted_email_code": post_data.fronted_email_code,
                "cellphone": post_data.cellphone or 110,
                "description": post_data.description,
            }
            Register.objects.create(**user_data)
        except Exception as e:
            "UNIQUE constraint failed: user_register.cellphone"
            unique = "UNIQUE" in str(e)
            reason = Dict()
            reason.cellphone = "您输入的手机号已被注册"
            reason.username = "您输入的用户名已被注册"
            reason.email = "您输入的邮箱号已被注册"
            if unique:
                import re

                resp_data.ErrMsg = reason.get(
                    re.search(r"user_register\.(.+)", str(e)).group(1), str(e)
                )
            else:
                resp_data.ErrMsg = str(e)
            logger.error(str(e))
            resp_data.ResCode = -1
            resp_data.desc = "FAILURE"
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def send_email_code(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            resp_data.email = post_data.email
            resp_data.email_code = Sender(person=post_data.email).main()
            Sender(person=post_data.email).main()
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            if 'authentication' in str(e):
                resp_data.ErrMsg = '系统发送验证码所用邮箱用户密码认证失败'
            resp_data.desc = "FAILURE"
            logger.error(str(e))
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def login(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            try:
                fetch_result = Register.objects.get(username=post_data.username.strip())
                logger.debug("password: {}".format(fetch_result.password))
                if fetch_result.password == post_data.password:
                    # 登陆成功 django
                    # request.session["login_name"] = post_data.username
                    # request.session.set_expiry(60 * 1)
                    resp_data.login_code = 0
                    resp_data.user_token = generator(
                        "username{}&password{}".format(post_data.username, post_data.password), expire=2 * 60 * 60)

                    # __key = lambda x, y: ("username={}&password={}".format(x, y))
                    # key = __key(post_data.username, post_data.password)
                    # resp_data.token = Token(key).generator(expire=3 * 6)
                    # resp_data.key = key
                else:
                    # 密码不正确
                    resp_data.login_code = 1
            except Exception as e:
                if "Register matching query does not exist" in str(e):
                    resp_data.login_code = 2
                    logger.debug(str(e))
                else:
                    resp_data.login_code = 3
                    resp_data.user_login_err = str(e)
                logger.error(str(e))
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(e))
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def verify_token(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            __key = lambda x, y: ("username={}&password={}".format(x, y))
            resp_data.token_alive = Token(
                __key(post_data.username, post_data.password)
            ).verify(post_data.token)
            resp_data.post_data = post_data
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(e))
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def modify_password(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            fetch_email = Register.objects.get(email=post_data.email)
            logger.debug("fetch: {}".format(fetch_email))
            Register.objects.filter(email=post_data.email).update(
                password=post_data.password
            )
            resp_data.post_data = post_data
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            if "Register matching query does not exist." in str(e):
                resp_data.ErrMsg = "根据邮箱号未在系统中查询到此用户，请注册！"
            resp_data.desc = "FAILURE"
            logger.error(str(e))
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)
