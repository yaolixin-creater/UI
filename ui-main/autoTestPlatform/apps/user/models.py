from django.db import models
import time

# Create your models here.


class Register(models.Model):
    '''Register'''
    register_id = models.IntegerField(primary_key=True)
    uuid = models.CharField(
        max_length=256 * 256,
        unique=True,
        default=None,
    )
    username = models.CharField(
        max_length=256,
        unique=True,
        null=False,
    )
    password = models.CharField(max_length=256, null=False,)
    gender = models.CharField(max_length=128)
    email = models.CharField(max_length=256, unique=True,)
    cellphone = models.IntegerField(
        null=True,
        unique=True,
        default=int(time.strftime("%Y%m%d%H%M%S", time.localtime())),
    )
    fronted_email_code = models.CharField(null=False,
                                          max_length=256,
                                          default=None)
    description = models.CharField(
        max_length=256 * 256,
        default=None,
    )
    create_time = models.CharField(
        max_length=256,
        null=False,
        default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    )
    update_time = models.CharField(
        max_length=256,
        null=False,
        default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    )

    def __str__(self):
        return self.username


class Image(models.Model):
    ''' 用户头像 '''
    image_id = models.IntegerField(primary_key=True)
    uuid = models.CharField(
        max_length=256 * 256,
        unique=True,
        default=None,
    )
    image_path = models.ImageField(upload_to='user_img')
    image_name = models.CharField(max_length=256, unique=False,)
    image_size = models.CharField(
        max_length=256,
        unique=False,
        default=None,
    )
    create_time = models.CharField(
        max_length=256,
        null=False,
        default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    )
    update_time = models.CharField(
        max_length=256,
        null=False,
        default=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    )

    def __str__(self):
        return self.image_name
