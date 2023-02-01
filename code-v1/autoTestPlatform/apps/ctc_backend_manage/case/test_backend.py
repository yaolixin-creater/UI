import json
import logging
import os
import sys
import datetime
import re

import django
import time
from addict import Dict
from django.core import serializers

logger = logging.getLogger("autotest")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoTestPlatform.settings")
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(PATH)
django.setup()

from apps.ctc_backend_manage.models import Case, Step, Item, LoginResult, EnvManagement
from apps.ctc_backend_manage.case.selenium_function import SeleniumFunction as sf
import pytest
from django.db.models import Q

g_extend_param_func = Dict()
g_extend_param_cls = Dict()


@pytest.fixture(scope="function", autouse=True)
def extend_param_func(request):
    global g_extend_param_func
    g_extend_param_func.casename = request.config.getoption("--casename")
    g_extend_param_func.report_id = request.config.getoption("--report_id")
    g_extend_param_func.env = request.config.getoption("--env")
    return g_extend_param_func


@pytest.fixture(scope="class", autouse=True)
def extend_param_cls(request):
    global g_extend_param_cls
    g_extend_param_cls.group = request.config.getoption("--group")
    g_extend_param_cls.env = request.config.getoption("--env")
    g_extend_param_cls.extend = request.config.getoption("--extend")
    return g_extend_param_cls


class Query:
    def __init__(self, group=None, env=None):
        self.group = group
        self.env = env

    def case(self):
        if len(self.group) == 1 and "全部" in self.group or not len(self.group):
            if self.env != "all":
                query_set = Case.objects.filter(
                    case_env__in=["general", self.env], case_seq=None
                )
            else:
                query_set = Case.objects.filter(case_seq=None)
        else:
            if self.env == "all":
                query_set = Case.objects.filter(
                    Q(case_type__in=self.group), Q(case_seq=None)
                )
            else:
                query_set = Case.objects.filter(
                    Q(case_type__in=self.group),
                    Q(case_env__in=["general", self.env]),
                    Q(case_seq=None),
                )
        query_case_data = json.loads(serializers.serialize("json", query_set))
        for case in query_case_data:
            yield Dict(case["fields"])

    def step(self, case_func):
        logger.debug("case_func: {}".format(case_func))
        query_step_data = json.loads(
            serializers.serialize(
                "json", Step.objects.filter(case_func=case_func).order_by("step_seq")
            )
        )
        for i in query_step_data:
            yield Dict(i["fields"])

    def get_case_by_env(self, case_env):
        case_func = str(
            Case.objects.filter(
                case_env=case_env, case_seq='ignore', case_type='前置'
            ).first().case_func)
        return case_func

    def get_host_by_env(self, case_env):
        host = str(
            EnvManagement.objects.filter(
                Env_name=case_env).first().host)
        return host


def pytest_generate_tests(metafunc):
    group = metafunc.config.getoption("group")
    env = metafunc.config.getoption("env")
    ids = [i.case_func for i in Query(group=group, env=env).case()]
    logger.debug("ids: {}".format(ids))
    metafunc.parametrize(
        argnames="case", argvalues=Query(group=group, env=env).case(), ids=ids
    )


user_interface = sf()


class TestBackend:
    @classmethod
    def setup_class(cls):
        login_result = "success"
        err_msg = ""

        try:
            logger.info("执行登陆...")
            logger.debug("setup class data: {}".format(g_extend_param_cls))
            case_func = Query().get_case_by_env(g_extend_param_cls.env)
            Step.objects.filter(**({'step_seq': 1, 'case_func': case_func})).update(
                action_value=re.sub(r'//(.*?)/', f"//{Query().get_host_by_env(g_extend_param_cls.env)}/",
                                    Step.objects.filter(**({'step_seq': 1,
                                                            'case_func': case_func})).first().action_value))
            for step in Query().step(
                    case_func=case_func
            ):
                user_interface.operate_all_actions(step)
        except Exception as e:
            err_msg = str(e)
            login_result = "failure"
            logger.error("登陆失败! \nerror messgae: \n{}".format(err_msg))
            user_interface.driver.get_screenshot_as_file(
                os.path.join(os.path.dirname(__file__), "screenshot", "login.png")
            )
        finally:
            try:
                param = Dict()
                param.result = login_result
                param.desc = "{}".format(err_msg)
                LoginResult.objects.filter(name="login").update(**param)
                if login_result != "success":
                    user_interface.driver.quit()
                    pytest.skip(allow_module_level=True)
            except Exception as e:
                logger.error(str(e))

    def teardown_method(self, method):
        pass

    def test_all_cases(self, case, extend_param_func):
        result = True
        flag = ["NRCC"]
        err_msg = desc = ""
        setattr(
            self.test_all_cases.__func__,
            "__doc__",
            "{}::{}".format(case.case_type, case.case_name),
        )
        try:
            logger.debug("extend param in case: {}".format(extend_param_func))
            logger.info("执行用例：【{}】【{}】".format(case.case_type, case.case_name))
            action_step = []
            for step in Query().step(case_func=case.case_func):
                action_step.append(step["ele_action"])
                if "assert" in step["ele_action"]:
                    flag = user_interface.operate_all_actions(step)
                    if str(flag[0]) == "200" or str(flag[0]) == "nonneed":
                        # logger.info("用例【{}】测试成功...\n{}".format(case.case_name, str(flag)))
                        result = True
                    else:
                        logger.info("用例测试失败，即将截图。。。")
                        result = False
                        raise Exception("用例断言失败")
                    assert result
                elif step["ele_action"] == "refresh_get_url":
                    host = Query().get_host_by_env(g_extend_param_cls.env)
                    user_interface.refresh_get_url(step, host)
                else:
                    user_interface.operate_all_actions(step)
            assert_flag = True
            for action in action_step:
                if "assert" in action:
                    assert_flag = False
                    break
            if assert_flag:
                flag = ["nonneed"]

        except Exception as e:
            result = False
            err_msg = str(e)
            user_interface.driver.get_screenshot_as_file(
                os.path.join(
                    os.path.dirname(__file__),
                    "screenshot",
                    "{}.png".format(
                        case.case_func.replace(" ", "_")
                            .replace("/", "_")
                            .replace("\\", "_")
                    ),
                )
            )
            user_interface.refresh_window()
            desc = "失败"
            logger.info(
                "用例【{}】测试失败; \n错误信息: \n{}; \n{}".format(
                    case.case_name, flag, err_msg
                )
            )
        finally:
            setattr(self.test_all_cases.__func__, "__str__", str(flag[0]))

            def item_to_registry():
                param = Dict()
                param.report_id = extend_param_func.report_id
                param.env = "None"
                param.env = extend_param_func.env
                param.casename = case.case_name
                param.method = case.case_func
                param.case_tested = 1
                param.err_msg = str(err_msg) or "None"
                param.result = result
                param.TransactionID = str(flag[0])
                param.desc = desc
                param.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                param.remark = "None"
                logger.debug("item params: {}".format(param))
                Item.objects.create(**param)

            try:
                item_to_registry()
            except Exception as e:
                logger.error(str(e))
        assert (
                   "200" if str(flag[0]) == "nonneed" else str(flag[0])
               ) in ["200", "201"] and result

    @classmethod
    def teardown_class(cls):
        logger.info("所有用例已经执行完毕, 关闭浏览器...")
        user_interface.driver.quit()


if __name__ == "__main__":
    PATH = os.path.dirname(__file__)
    command = "pytest46 test_backend.py --html={} --self-contained-html \
        --capture=no ".format(
        os.path.join(PATH, "backend_report.html")
    )
    os.chdir(PATH)
    os.system(command)
