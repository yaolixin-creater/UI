# Create your views here.
import importlib
import itertools
import json
import logging
import os
import sys
import threading
import time
import tracemalloc
# from concurrent.futures import (ALL_COMPLETED, FIRST_COMPLETED,
#                                 FIRST_EXCEPTION, ProcessPoolExecutor,
#                                 ThreadPoolExecutor, wait)
from multiprocessing import Pool
from threading import Thread
from addict import Dict
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from ..user.auth_token import AuthToken
from ..ctc_backend_manage.case.executor import Executor
from ..ctc_backend_manage.case.selenium_function import operation_map
from .models import Case, Step, Reporter, Item, LoginResult, GroupManagement, EnvManagement
from django.db.models import Q, Max
from apscheduler.scheduler import Scheduler

sched = Scheduler()
BASE_DIR = os.path.dirname(__file__)
logger = logging.getLogger("autotest")


# threadingPool = ThreadPoolExecutor(max_workers=os.cpu_count())

def __jsoner(resp_data):
    return HttpResponse(
        json.dumps(resp_data),
        content_type="application/json; charset=utf-8",
        status=200,
    )


def db_backup(case_func, del_step):
    import platform
    manage_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../', 'manage.py'))
    pyexe_local = f'{os.sys.executable}'
    pyexe_other = f'{os.sys.executable}'
    os.chdir(os.path.dirname(__file__))
    # os.system('"{}" {}'.format(pyexe_local, manage_file))
    os.system('"{}" {} dumpdata --indent 2 --exclude corsheaders \
                --exclude contenttypes --exclude auth.permission > \
                    bak/db_del_{}_{}s_{}.json'.format(
        (pyexe_local if platform.node() == 'LAPTOP-Q4JQTDKJ' else pyexe_other),
        manage_file,
        case_func.replace('/', '_').replace('\\', '_'),
        del_step,
        time.strftime("%Y%m%d%H%M%S", time.localtime()),
    ))


@csrf_exempt
def run_test(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.ResCode = 0
    resp_data.ResDesp = "SUCCESS"
    try:
        if request.method == "POST":
            data = Dict(json.loads(request.body.decode()))
            logger.info("Post data: {}".format(data))
            host = str(EnvManagement.objects.filter(Env_name=data.env).first().host)
            # Step.objects.filter(**({
            #                            'step_seq': 1,
            #                            'case_func': 'login'
            #                        } if data.env == 'test' else {
            #     'step_seq': 1,
            #     'case_func': 'login_production'
            # })).update(action_value=(
            #     'http://{}/#/login/'.format(data.host) if data.env ==
            #                                               'test' else 'http://{}/login/'.format(data.host)))
            exe = Executor(data=data)
            resp_data.ReportUrl = "/backendManage/getReport/{}".format(
                exe.report_name)
            resp_data.report_id = exe.report_id or None

            t = Thread(target=exe.executor)
            t.start()

    except Exception as e:
        resp_data.ResDesp = "FAILURE"
        resp_data.ResCode = -1
        resp_data.ErrMsg = str(e)
        logger.error(str(e))

    finally:

        def reporter_create():
            param = {
                "report_id": exe.report_id or None,
                "name": exe.report_name,
                "url": resp_data.ReportUrl,
                "env": data.env,
                "host": host,
                "casename": data.casename or None,
                # "corenum": data.corenum,
                "err_msg": resp_data.ErrMsg or None,
                "remark": data.desc or None,
                "desc": resp_data.ResDesp or None,
                "create_time": time.strftime("%Y-%m-%d %H:%M:%S",
                                             time.localtime())
            }
            logger.debug("param: {}".format(param))
            Reporter.objects.create(**param)
            resp_data.postData = param

        reporter_create()

    return __jsoner(resp_data)


@csrf_exempt
def get_report(request, report_name):
    resp_data = Dict()
    resp_data.ResCode = 0
    logger.debug(request.get_full_path())
    logger.debug("Report_name: {}".format(report_name))
    try:
        if request.method == "GET":
            return render(request,
                          "html_report/{}".format(report_name),
                          status=200)
    except Exception as e:
        ErrMsg = str(e) + ' not exists'
        logger.error(ErrMsg)
        resp_data.ErrMsg = ErrMsg
        resp_data.ResCode = -1
        return __jsoner(resp_data)


@csrf_exempt
def query_report(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    conditions = Dict()
    resp_data.ResCode = 0
    try:
        if request.method == "POST":
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            if len(post_data.report_id):
                conditions = {"report_id": post_data.report_id}
            else:
                conditions.report_id = post_data.report_id or ""
                conditions.env = post_data.env or ""
                conditions.env_Name = post_data.env_Name or ""
                conditions.remark = post_data.desc or ""
                logger.debug("conditions data: {}".format(conditions))
                for key in list(conditions.keys()):
                    if not conditions.get(key):
                        del conditions[key]
            start_time = post_data.start_time or "2000-01-01"
            end_time = post_data.end_time or "3000-01-01"
            query_data = json.loads(
                serializers.serialize(
                    "json",
                    Reporter.objects.filter(
                        create_time__range=[start_time, end_time],
                        **conditions).order_by("-create_time"),
                ))
            resp_data.data = query_data
            logger.debug(resp_data)
    except Exception as e:
        resp_data.ErrMsg = str(e)
        resp_data.ResCode = -1
    return __jsoner(resp_data)


@csrf_exempt
def get_case_argvs(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            resp_data.argvs = operation_map
            operation_method = list()
            for key in resp_data.argvs:
                operation_method.append(key)
            resp_data.operation_method = sorted(operation_method)
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(e))
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def add_case_argvs(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.info("post data: {}".format(post_data))
            param = {
                'case_name':
                    post_data.casename or None,
                'case_func':
                    post_data.case_func or None,
                'case_seq': ('ignore' if (('login' in post_data.case_func)
                                          and post_data.case_type == '前置') else None),
                'case_type':
                    post_data.case_type or None,
                'case_env':
                    post_data.case_env,
                "create_time":
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'remark':
                    post_data.caseRemark or None,
            }
            if post_data.case_type == "前置":
                try:
                    if Case.objects.filter(case_env=post_data.case_env, case_type="前置").exists():
                        if Case.objects.filter(case_func=post_data.case_func, case_name=post_data.casename).exists():
                            Case.objects.filter(
                                case_func=str(post_data.case_func)).update(**param)
                        else:
                            resp_data.ResCode = -1
                            raise Exception(f'该环境下{post_data.case_env}已存在前置用例，请核实...')
                except Exception as e:
                    raise Exception(str(e))
            else:
                pass
            if Case.objects.filter(case_func=str(
                    post_data.case_func)).exists() or Case.objects.filter(
                case_name=str(post_data.casename)).exists():
                casename = ''
                try:
                    casename = str(
                        Case.objects.filter(case_func=str(
                            post_data.case_func)).first().case_name)
                    logger.debug(casename)
                except Exception as e:
                    if 'NoneType' in str(e):
                        resp_data.ResCode = -1
                        raise Exception('该用例名【{}】已经存在，请重新指定...'.format(
                            post_data.casename))
                    else:
                        resp_data.ResCode = -1
                        raise Exception(str(e))
                if casename == str(post_data.casename):
                    Case.objects.filter(
                        case_func=str(post_data.case_func)).update(**param)
                else:
                    resp_data.ResCode = -1
                    raise Exception('请指定正确用例名; 【{}】'.format(casename))
            else:
                Case.objects.create(**param)
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(e))
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def add_step_argvs(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            param = {
                'step_seq_case_func':
                    '{}_{}'.format(
                        str(post_data.step_seq),
                        str(post_data.case_func),
                    ),
                'case_name':
                    post_data.casename or None,
                'case_func':
                    post_data.case_func or None,
                'step_seq':
                    post_data.step_seq or None,
                'action_desc':
                    post_data.action_desc or None,
                'ele_action':
                    post_data.ele_action or None,
                'loc_type':
                    post_data.locate_type or None,
                'loc_value':
                    post_data.locate_value or None,
                'action_value':
                    post_data.action_value or None,
                'argvs':
                    str(post_data.argvs) or None,
                'assert_value':
                    post_data.assert_value or None,
                'remark':
                    post_data.remark or None,
                "create_time":
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
            logger.debug(param)
            Step.objects.create(**param)
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            if 'UNIQUE constraint failed: ctc_backend_manage_step.step_seq_case_func' in str(
                    e):
                resp_data.ErrMsg = '用例【{}】||【{}】第【{}】步配置已经存在...'.format(
                    str(post_data.casename),
                    str(post_data.case_func),
                    str(post_data.step_seq),
                )
            resp_data.desc = "FAILURE"
            logger.error(str(resp_data.ErrMsg))
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def add_step_through_insert(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            param = {
                'step_seq_case_func':
                    '{}_{}'.format(
                        str(post_data.step_seq),
                        str(post_data.case_func),
                    ),
                'case_name':
                    post_data.casename,
                'case_func':
                    post_data.case_func,
                'step_seq':
                    post_data.step_seq or None,
                'action_desc':
                    post_data.action_desc,
                'ele_action':
                    post_data.ele_action or None,
                'loc_type':
                    post_data.locate_type or None,
                'loc_value':
                    post_data.locate_value or None,
                'action_value':
                    post_data.action_value or None,
                'argvs':
                    str(post_data.argvs) or None,
                'assert_value':
                    post_data.assert_value or None,
                'remark':
                    post_data.remark or None,
                "create_time":
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
            logger.debug(param)
            steps = len(Step.objects.filter(case_func=post_data.case_func))
            if post_data.step_seq > steps + 1:
                raise Exception(
                    '您添加的步骤为第【{}】步; 当前用例只有【{}】个步骤，最大添加步骤应为【{}】'.format(
                        post_data.step_seq, steps, steps + 1))
            elif post_data.step_seq == steps + 1:
                Step.objects.create(**param)
            elif post_data.step_seq < steps + 1:
                case_step = json.loads(
                    serializers.serialize(
                        "json",
                        Step.objects.filter(case_func=post_data.case_func).
                            order_by("step_seq")))
                for order in range(post_data.step_seq - 1, steps):
                    case_step[order]['fields']['step_seq'] = order + 2
                    del case_step[order]['fields']['step_seq_case_func']
                    logger.debug('{}: {}'.format(order + 2,
                                                 case_step[order]['fields']))
                    if (order + 2) != steps + 1:
                        Step.objects.filter(step_seq_case_func='{}_{}'.format(
                            order + 2, post_data.case_func)).update(
                            **case_step[order]['fields'])
                    else:
                        case_step[order]['fields'][
                            'step_seq_case_func'] = '{}_{}'.format(
                            order + 2, post_data.case_func)
                        Step.objects.create(**case_step[order]['fields'])
                Step.objects.filter(
                    step_seq_case_func=param['step_seq_case_func']).update(
                    **param)
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(resp_data.ErrMsg))
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def del_case_step(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            del_step = post_data.index + 1
            # threadingPool.submit(db_backup)
            db_backup(case_func=post_data.case_func,
                      del_step=post_data.index + 1)
            steps = len(Step.objects.filter(case_func=post_data.case_func))
            if del_step == steps:
                Step.objects.filter(case_func=post_data.case_func,
                                    step_seq=del_step).delete()
            elif del_step < steps:
                case_step = json.loads(
                    serializers.serialize(
                        "json",
                        Step.objects.filter(case_func=post_data.case_func).
                            order_by("step_seq")))
                for order in range(del_step, steps):
                    case_step[order]['fields']['step_seq'] = order
                    del case_step[order]['fields']['step_seq_case_func']
                    logger.debug('{}: {}'.format(order,
                                                 case_step[order]['fields']))
                    Step.objects.filter(step_seq_case_func='{}_{}'.format(
                        order, post_data.case_func)).update(
                        **case_step[order]['fields'])
                Step.objects.filter(step_seq_case_func='{}_{}'.format(
                    steps, post_data.case_func)).delete()
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(resp_data.ErrMsg))
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def query_case_name(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            conditions = Dict()
            conditions.case_func = post_data.case_func or ""
            conditions.case_type = post_data.case_type or ""
            conditions.case_env = post_data.env or ""
            conditions.remark = post_data.remark or ""
            for key in list(conditions.keys()):
                if not conditions.get(key):
                    del conditions[key]
            if post_data.page_type == 'caselist':
                conditions.case_seq = None
            logger.debug("conditions data: {}".format(conditions))
            start_time = post_data.start_time or "2000-01-01"
            end_time = post_data.end_time or "3000-01-01"
            logger.debug('{} 至 {}'.format(start_time, end_time))
            query_case_data = json.loads(
                serializers.serialize(
                    "json",
                    Case.objects.filter(
                        create_time__range=[start_time, end_time],
                        **conditions).order_by("-create_time"),
                ))
            resp_data.query_case_data = query_case_data
            if not len(query_case_data):
                raise Exception('查询结果为空')
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def query_case_step(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            data = Dict()
            if str(post_data.query_type) != 'all':
                data.case_func = post_data.case_func
            case_step = json.loads(
                serializers.serialize(
                    "json",
                    Step.objects.filter(**data).order_by("step_seq"),
                ))
            for index, i in enumerate(case_step, 0):
                case_step[index]['fields']['argvs_quotes_sd'] = json.dumps(
                    eval(i['fields']['argvs']))
                logger.debug(case_step[index])
            resp_data.step_count = len(case_step)
            resp_data.case_step = case_step
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def query_present_step(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            steps = len(Step.objects.filter(case_func=post_data.case_func))
            resp_data.step_count = steps
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def update_step_for_move(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))

            def query_step_data(data_id=0):
                data = post_data.step_move[data_id]
                step_data = json.loads(
                    serializers.serialize(
                        "json",
                        Step.objects.filter(step_seq_case_func='{}_{}'.format(
                            data['old_step_seq'], data['case_func']))))
                logger.debug(step_data)
                new_step_data = step_data[0]['fields']
                new_step_data['step_seq_case_func'] = '{}_{}'.format(
                    data['new_step_seq'], data['case_func'])
                new_step_data['step_seq'] = data['new_step_seq']
                step_seq_case_func = new_step_data['step_seq_case_func']
                del new_step_data['step_seq_case_func']
                return step_seq_case_func, new_step_data

            present_pk, present_data = query_step_data()
            _pk, _data = query_step_data(data_id=1)
            logger.debug('{}; {}'.format(present_pk, _pk))
            Step.objects.filter(step_seq_case_func=present_pk).update(
                **present_data)
            Step.objects.filter(step_seq_case_func=_pk).update(**_data)
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            logger.error(str(e))
            resp_data.desc = "FAILURE"
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def modify_step_argvs(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            param = {
                'step_seq_case_func':
                    '{}_{}'.format(
                        str(post_data.step_seq),
                        str(post_data.case_func),
                    ),
                'case_name':
                    post_data.casename or None,
                'case_func':
                    post_data.case_func or None,
                'step_seq':
                    post_data.step_seq or None,
                'action_desc':
                    post_data.action_desc or None,
                'ele_action':
                    post_data.ele_action or None,
                'loc_type':
                    post_data.locate_type or None,
                'loc_value':
                    post_data.locate_value or None,
                'action_value':
                    post_data.action_value or None,
                'argvs':
                    str(post_data.argvs) or None,
                'assert_value':
                    post_data.assert_value or None,
                'remark':
                    post_data.remark or None,
                "update_time":
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
            logger.debug(param)
            Step.objects.filter(
                step_seq_case_func=param['step_seq_case_func']).update(**param)
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(resp_data.ErrMsg))
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def modify_case_argvs(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            param = {
                'case_name':
                    post_data.casename or None,
                'case_func':
                    post_data.case_func or None,
                'case_seq': ('ignore' if (('login' in post_data.case_func)
                                          and post_data.case_type == '前置') else None),
                'case_type':
                    post_data.case_type or None,
                'case_env':
                    post_data.case_env,
                'remark':
                    post_data.caseRemark or None,
                "update_time":
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
            logger.debug(param)
            Case.objects.filter(case_func=post_data.case_func).update(**param)
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(e))
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def query_case_tested(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    if request.method == "POST":
        post_data = Dict(json.loads(request.body.decode()))
        logger.debug("post data: {}".format(post_data))
        query_item = Item.objects.filter(
            report_id=post_data.report_id).order_by("-create_time")
        count = 0
        count_failed = 0
        for i in query_item:
            logger.debug('query result: {}'.format(type(i.result)))
            if i.result:
                count += 1
            else:
                count_failed += 1
        query_data = json.loads(serializers.serialize(
            "json",
            query_item,
        ))
        resp_data.case_tested_count = len(query_data)
        resp_data.pass_count = count
        resp_data.fail_count = count_failed
        logger.debug(resp_data)
    resp_data.ResCode = 0
    return __jsoner(resp_data)


@csrf_exempt
def query_summary(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            query_data = json.loads(
                serializers.serialize(
                    "json",
                    Item.objects.filter(
                        report_id=post_data.reportId).order_by("-result"),
                ))
            resp_data.query_data = query_data
            resp_data.post_data = post_data
            resp_data.query_data_count = len(query_data)
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def get_login_result(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            query_data = Dict(
                json.loads(
                    serializers.serialize(
                        "json",
                        LoginResult.objects.filter(name='login'),
                    ))[0])
            resp_data.query_data = query_data.fields
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def init_login_result(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            LoginResult.objects.filter(name="login").update(result='init')
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def write_mobile_pcc(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            Step.objects.filter(
                ele_action="wait_mobile_certification_code",
                case_func='login_production').update(
                action_value=(None if post_data.type ==
                                      'init' else post_data.action_value or None))
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def delete_case_all_steps(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            db_backup(case_func=post_data.case_func, del_step='all')
            try:
                Case.objects.filter(case_func=post_data.case_func).delete()
                Step.objects.filter(case_func=post_data.case_func).delete()
            except Exception as e:
                logging.warning(str(e))
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def query_group_case(request):
    # add case env filtered
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            group = post_data.group
            env = post_data.env
            logger.debug('env: {}'.format(env))
            if len(group) == 1 and '全部' in group or not len(group):
                if env != 'all':
                    query_set = Case.objects.filter(
                        case_env__in=['general', env],
                        case_seq=None,
                    )
                else:
                    query_set = Case.objects.filter(case_seq=None)
            else:
                if env == 'all':
                    query_set = Case.objects.filter(
                        Q(case_type__in=group),
                        Q(case_seq=None),
                    )
                else:
                    query_set = Case.objects.filter(
                        Q(case_type__in=group),
                        Q(case_env__in=['general', env]),
                        Q(case_seq=None),
                    )
            query_case_data = json.loads(
                serializers.serialize("json", query_set))
            resp_data.query_case_data = query_case_data
            if not len(query_case_data):
                raise Exception('亲，根据所选分组未查询到用例...')
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            logger.error(str(e))
            resp_data.desc = "FAILURE"
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def query_step_accord_desc(request):
    logger.debug(request.get_full_path())
    resp_data = Dict()
    resp_data.desc = "SUCCESS"
    resp_data.ResCode = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            query_data = json.loads(
                serializers.serialize(
                    "json",
                    Step.objects.filter(action_desc__icontains=str(
                        post_data.actionDesc or ''))))
            resp_data.query_data_count = len(query_data)
            resp_data.query_data = query_data
            if not len(query_data):
                raise Exception('亲，根据动作描述未查询到数据...')
        except Exception as e:
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
            logger.error(str(e))
            resp_data.desc = "FAILURE"
    logger.debug("resp data: {}".format(resp_data))
    return __jsoner(resp_data)


@csrf_exempt
def del_report(request):
    resp_data = Dict()
    resp_data.ResCode = 0
    logger.debug(request.get_full_path())
    if request.method == "POST":
        data = Dict(json.loads(request.body.decode()))
        logger.debug("post data: {}".format(data))
        try:
            Reporter.objects.filter(report_id=data.report_id).delete()
            Item.objects.filter(report_id=data.report_id).delete()
            resp_data.dbMesg = "数据库中记录已经被删除..."
            os.remove(
                os.path.join(
                    os.path.dirname(__file__),
                    "templates",
                    "html_report",
                    "test_report_{}.html".format(data.report_id),
                ).replace("\\", "/"))
            resp_data.fileMesg = "HTML删除成功"
        except Exception as e:
            logger.error(str(e))
            resp_data.ResCode = -1
            resp_data.ErrMsg = '未生成HTML' if '系统找不到指定的文件。:' in str(e) else str(
                e)
    return __jsoner(resp_data)


@csrf_exempt
def modify_steps(request):
    resp_data = Dict()
    resp_data.ResCode = 0
    logger.info(request.get_full_path())
    if request.method == "POST":
        data = Dict(json.loads(request.body.decode()))
        logger.debug("post data: {}".format(data))
        try:
            steps = Step.objects.filter(action_desc=data.action_desc, loc_value=data.locate_value).update(
                loc_value=data.locate_value_new)
            logger.info(steps)
            resp_data.lens = steps
        except Exception as e:
            logger.error(str(e))
            resp_data.ResCode = -1
            resp_data.ErrMsg = str(e)
    return __jsoner(resp_data)


# { desc: '第一步', order: 1 }
@csrf_exempt
def get_step_dict(request):
    resp_data = Dict()
    resp_data.code = 0
    logger.info(request.get_full_path())
    if request.method == "POST":
        try:
            max_step = Step.objects.aggregate(Max('step_seq')).get("step_seq__max")
            step_item = max_step / 100
            if isinstance(step_item, int):
                step_item += 1
            else:
                step_item = int(max_step / 100) + 1
            data = Dict(json.loads(request.body.decode()))
            num_instance = int(data.num_instance) if data.num_instance else 100 * step_item
            step_dict = [{"desc": f"第{each + 1}步", "order": each + 1} for each in range(num_instance)]
            resp_data.steps_list = step_dict
        except Exception as e:
            logger.error(str(e))
            resp_data.code = -1
            resp_data.ErrMsg = str(e)
    return __jsoner(resp_data)


@csrf_exempt
def get_memory(request):
    resp_data = Dict()
    resp_data.code = 0
    if request.method == "POST":
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        # resp_data.data = str(top_stats[:10])
        for index, each in enumerate(top_stats[:10]):
            resp_data.dict[f"top{index + 1}"] = str(each)
    print(resp_data)
    return __jsoner(resp_data)


@csrf_exempt
def create_group(request):
    resp_data = Dict()
    resp_data.code = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.info("post data: {}".format(post_data))
            param = {
                'group_name':
                    post_data.addGroupName or None,
                'desc':
                    post_data.addGroupDesc or None,
                "create_time":
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'owner':
                    post_data.addOwner or None,
            }
            if GroupManagement.objects.filter(group_name=str(post_data.group_name)).exists():
                try:
                    group_name = str(
                        GroupManagement.objects.filter(group_name=str(
                            post_data.group_name)).first().group_name)
                    logger.debug(group_name)
                except Exception as e:
                    if 'NoneType' in str(e):
                        resp_data.ResCode = -1
                        raise Exception('该分组【{}】已经存在，请重新指定...'.format(
                            post_data.group_name))
                    else:
                        resp_data.ResCode = -1
                        raise Exception(str(e))
                else:
                    resp_data.ResCode = -1
                    raise Exception('请指定正确分组名; 【{}】'.format(group_name))
            else:
                GroupManagement.objects.create(**param)
        except Exception as e:
            resp_data.code = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "CREATE FAILURE"
            logger.error(str(e))
    return __jsoner(resp_data)


@csrf_exempt
def show_groups(request):
    resp_data = Dict()
    resp_data.code = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            query_data = json.loads(
                serializers.serialize(
                    "json",
                    GroupManagement.objects.all()))
            group_list = [Dict(each).fields.group_name for each in query_data]
            logger.debug(group_list)
            resp_data.data = group_list

        except Exception as e:
            resp_data.code = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(e))
    return __jsoner(resp_data)


@csrf_exempt
def show_groups_details(request):
    resp_data = Dict()
    resp_data.code = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            search_group_name = post_data.search_group_name or None
            if not search_group_name:
                query_data = json.loads(
                    serializers.serialize(
                        "json",
                        GroupManagement.objects.all()))
            else:
                query_data = json.loads(
                    serializers.serialize(
                        "json",
                        GroupManagement.objects.filter(group_name=search_group_name)))
            group_details = []
            for each in query_data:
                each.get("fields", {})["group_id"] = each.get("pk")
                if each.get("fields").get("group_name") != '前置':
                    group_details.append(each.get("fields"))
            resp_data.data = group_details

        except Exception as e:
            resp_data.code = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(e))
    return __jsoner(resp_data)


@csrf_exempt
def mod_group_name(request):
    resp_data = Dict()
    resp_data.code = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            group_name = post_data.group_name
            m_group_name = post_data.m_group_name
            m_group_desc = post_data.m_group_desc
            GroupManagement.objects.filter(group_name=group_name).update(group_name=m_group_name, desc=m_group_desc)
            Case.objects.filter(case_env=group_name).update(case_env=m_group_name)
        except Exception as e:
            resp_data.code = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(e))
    return __jsoner(resp_data)


@csrf_exempt
def del_group_name(request):
    resp_data = Dict()
    resp_data.code = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.info("post data: {}".format(post_data))
            if Case.objects.filter(case_type=post_data.group_name).exists():
                raise Exception('该分组下【{}】已存在用例，请核实...'.format(
                    post_data.group_name))
            else:
                GroupManagement.objects.filter(group_name=post_data.group_name).delete()
        except Exception as e:
            resp_data.code = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(e))
    return __jsoner(resp_data)


@csrf_exempt
def show_envs(request):
    resp_data = Dict()
    resp_data.code = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            if_all = post_data.IfAll or None
            query_data = json.loads(
                serializers.serialize(
                    "json",
                    EnvManagement.objects.all()))
            # env_list = [Dict(each).fields.Env_name for each in query_data]
            # [{'desc':desc,'Env_name': Env_name}]
            if not if_all:
                env_list = [{"desc": Dict(each).fields.desc, "Env_name": Dict(each).fields.Env_name}
                            for each in query_data if Dict(each).fields.Env_name != "general"]
            else:
                env_list = [{"desc": Dict(each).fields.desc, "Env_name": Dict(each).fields.Env_name} for
                            each in query_data]
            logger.debug(env_list)
            resp_data.data = env_list

        except Exception as e:
            resp_data.code = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(e))
    return __jsoner(resp_data)


@csrf_exempt
def show_envs_details(request):
    resp_data = Dict()
    resp_data.code = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            search_group_name = post_data.search_group_name or None
            if not search_group_name:
                query_data = json.loads(
                    serializers.serialize(
                        "json",
                        EnvManagement.objects.all()))
            else:
                query_data = json.loads(
                    serializers.serialize(
                        "json",
                        EnvManagement.objects.filter(Env_name=search_group_name)))
            group_details = []
            for each in query_data:
                if each.get("fields", {})["Env_name"] != 'general':
                    each.get("fields", {})["Env_id"] = each.get("pk")
                    group_details.append(each.get("fields"))
            resp_data.data = group_details

        except Exception as e:
            resp_data.code = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(e))
    return __jsoner(resp_data)


@csrf_exempt
def mod_env_name(request):
    resp_data = Dict()
    resp_data.code = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.debug("post data: {}".format(post_data))
            group_name = post_data.group_name
            m_group_name = post_data.m_group_name
            m_group_desc = post_data.m_group_desc
            m_group_host = post_data.m_group_host
            EnvManagement.objects.filter(Env_name=group_name).update(
                Env_name=m_group_name, desc=m_group_desc, host=m_group_host)
            Case.objects.filter(case_env=group_name).update(case_env=m_group_name)
        except Exception as e:
            resp_data.code = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(e))
    return __jsoner(resp_data)


@csrf_exempt
def del_env_name(request):
    resp_data = Dict()
    resp_data.code = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.info("post data: {}".format(post_data))
            # 删除之前，判断一下是否有存有实例，有则不能删除
            if Case.objects.filter(case_env=post_data.group_name).exists():
                raise Exception('该环境【{}】已存在用例，请核实...'.format(
                    post_data.group_name))
            else:
                EnvManagement.objects.filter(Env_name=post_data.group_name).delete()
        except Exception as e:
            resp_data.code = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "FAILURE"
            logger.error(str(e))
    return __jsoner(resp_data)


@csrf_exempt
def create_env(request):
    resp_data = Dict()
    resp_data.code = 0
    if request.method == "POST":
        try:
            post_data = Dict(json.loads(request.body.decode()))
            logger.info("post data: {}".format(post_data))
            param = {
                'Env_name':
                    post_data.addGroupName or None,
                'desc':
                    post_data.addGroupDesc or None,
                'host':
                    post_data.addGroupHost or None,
                "create_time":
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'owner':
                    post_data.addOwner or None,
            }
            if EnvManagement.objects.filter(Env_name=str(post_data.group_name)).exists():
                try:
                    group_name = str(
                        EnvManagement.objects.filter(Env_name=str(
                            post_data.group_name)).first().Env_name)
                    logger.debug(group_name)
                except Exception as e:
                    if 'NoneType' in str(e):
                        resp_data.ResCode = -1
                        raise Exception('该环境【{}】已经存在，请重新指定...'.format(
                            post_data.group_name))
                    else:
                        resp_data.ResCode = -1
                        raise Exception(str(e))
                else:
                    resp_data.ResCode = -1
                    raise Exception('请指定正确环境名; 【{}】'.format(group_name))
            else:
                EnvManagement.objects.create(**param)
        except Exception as e:
            resp_data.code = -1
            resp_data.ErrMsg = str(e)
            resp_data.desc = "CREATE FAILURE"
            logger.error(str(e))
    return __jsoner(resp_data)


def regularly_perform_by_daily():
    print("hello")


def regularly_perform_by_specified_day():
    pass


@sched.cron_schedule(hour=9, minute=58)
def my_task1():
    regularly_perform_by_daily()


sched.start()
