from django.db import models

import time


class Case(models.Model):
    '''BackendCase'''
    case_id = models.IntegerField(primary_key=True)
    case_name = models.CharField(
        max_length=256 * 256,
        unique=True,
        default=None,
    )
    case_func = models.CharField(
        max_length=256 * 256,
        unique=True,
        default=None,
    )
    # status_cd = models.BooleanField()
    # filter login data
    case_seq = models.CharField(
        max_length=256,
        default=None,
        null=True,
    )
    case_type = models.CharField(
        max_length=256,
        default=None,
        null=False,
    )
    case_env = models.CharField(
        max_length=256,
        default='general',
        null=False,
    )
    remark = models.CharField(
        max_length=256,
        null=True,
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
        return self.case_name


class Step(models.Model):
    '''Step'''
    step_id = models.IntegerField(primary_key=True)
    step_seq_case_func = models.CharField(
        max_length=256 * 256,
        unique=True,
        default=None,
    )
    case_name = models.CharField(
        max_length=256 * 256,
        unique=False,
        default=None,
    )
    case_func = models.CharField(
        max_length=256 * 256,
        unique=False,
        default=None,
    )
    step_seq = models.IntegerField(null=False, )
    action_desc = models.CharField(
        max_length=256,
        null=False,
    )
    ele_action = models.CharField(
        max_length=256,
        null=False,
    )
    loc_type = models.CharField(
        max_length=256,
        null=True,
    )
    loc_value = models.CharField(
        max_length=256,
        null=True,
    )
    action_value = models.CharField(
        max_length=256,
        null=True,
    )
    argvs = models.CharField(
        max_length=256 * 256 * 256,
        null=True,
    )
    assert_value = models.CharField(
        max_length=256,
        null=True,
    )
    remark = models.CharField(
        max_length=256,
        null=True,
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
        return self.action_desc


class Reporter(models.Model):
    """report"""

    report_id = models.CharField(max_length=128,
                                 unique=True,
                                 primary_key=True,
                                 null=False)
    name = models.CharField(max_length=256, unique=True)
    url = models.GenericIPAddressField(protocol="ipv4",
                                       null=False,
                                       unique=True)
    env = models.CharField(max_length=256)
    host = models.CharField(max_length=256, null=True)
    casename = models.CharField(null=True, max_length=256 * 256)
    corenum = models.IntegerField(null=True)
    err_msg = models.CharField(max_length=256 * 256 * 256,
                               null=True,
                               default=None)
    remark = models.CharField(max_length=256, null=True)
    desc = models.CharField(max_length=256, null=True)
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
        return self.name


class Item(models.Model):
    """Item"""

    process_id = models.IntegerField(primary_key=True)
    report_id = models.CharField(max_length=128, null=False)
    env = models.CharField(max_length=256, null=True)
    filename = models.CharField(max_length=256, null=True, default='None')
    casename = models.CharField(
        null=False,
        max_length=256 * 256,
    )
    method = models.CharField(
        null=False,
        max_length=256 * 256,
    )
    case_tested = models.IntegerField(null=True)
    err_msg = models.CharField(
        max_length=256,
        null=True,
        default=None,
    )
    result = models.BooleanField()
    TransactionID = models.CharField(
        max_length=256,
        null=True,
        default=None,
    )
    desc = models.CharField(max_length=256 * 256 * 256,
                            null=True,
                            default=None)
    remark = models.CharField(
        max_length=256,
        null=True,
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
        return self.report_id


class LoginResult(models.Model):
    """LoginResult"""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(
        max_length=128,
        null=False,
        unique=True,
    )
    # result = models.BooleanField()
    result = models.CharField(
        max_length=256,
        null=False,
    )
    desc = models.CharField(
        max_length=256 * 256,
        null=True,
    )
    remark = models.CharField(
        max_length=256,
        null=True,
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
        return self.name


class GroupManagement(models.Model):
    """GroupManagement"""

    group_id = models.IntegerField(primary_key=True)
    group_name = models.CharField(
        max_length=128,
        null=False,
        unique=True,
    )
    desc = models.CharField(
        max_length=256 * 256,
        null=True,
    )
    owner = models.CharField(
        max_length=256,
        null=True,
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
        return self.group_name


class EnvManagement(models.Model):
    """EnvManagement"""

    Env_id = models.IntegerField(primary_key=True)
    Env_name = models.CharField(
        max_length=128,
        null=False,
        unique=True,
    )
    desc = models.CharField(
        max_length=256 * 256,
        null=True,
    )
    owner = models.CharField(
        max_length=256,
        null=True,
    )
    host = models.CharField(
        max_length=256,
        null=True,
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
        return self.Env_name