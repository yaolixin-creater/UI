# coding:utf-8
import os, time
import logging
from apps.ctc_backend_manage.models import Case, Step
from django.db.models import Q
import json
from django.core import serializers


logger = logging.getLogger("autotest")
from addict import Dict
import uuid
import hashlib

class Executor:
    def __init__(self, data=None):
        self.data = data
        self.report_id = self.make_report_id()
        self.report_name = "test_report_{}.html".format(self.report_id)
        self.html_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "templates/html_report",
                self.report_name,
            )
        ).replace("\\", "/")
        self.pytest_logpath = os.path.join(
            os.path.dirname(__file__),
            "templates/html_report",
            "pytest_{}.log".format(time.strftime("%Y%m%d%H%M%S", time.localtime())),
        ).replace("\\", "/")

    def executor(self):
        """"组织命令行参数"""
        logger.info("data: {}".format(self.data))
        os.chdir(os.path.dirname(__file__))
        command = "pytest "
        command += "{} ".format("test_backend.py")
        command += "--html={} --self-contained-html ".format(self.html_dir)
        command += "--capture=no "
        command += "--pastebin=failed "
        # command += "-n {} ".format(
        #     (int(self.data.corenum) if (int(self.data.corenum) and int(self.data.corenum) <= 6) else 1)
        # )
        if self.case_len() > 2:
            command += "-n 2 "
        else:
            command += "-n 1 "
        # command += "-n 1 "
        for group in self.data.group:
            command += "--group {} ".format(group)
        command += "--env {} ".format(self.data.env)
        command += "--extend {} ".format(self.data.extend)
        for casename in self.data.casename:
            command += "--casename {} ".format(
                '"{}"'.format(casename) if " " in casename else casename
            )
        command += "--report_id {} ".format(self.report_id)
        logger.info(command)
        os.system(command)

    def make_report_id(self, lens=16):
        s = uuid.uuid1()
        m = hashlib.md5()
        m.update(str(s).encode("utf-8"))
        s = m.hexdigest()
        if lens == 16:
            return s[8:-8]
        else:
            return s

    def case_len(self):
        if self.data.casename:
            return len(self.data.casename)
        else:
            if len(self.data.group) == 1 and "全部" in self.data.group or not len(self.data.group):
                if self.data.env != "all":
                    query_set = Case.objects.filter(
                        case_env__in=["general", self.data.env], case_seq=None
                    )
                else:
                    query_set = Case.objects.filter(case_seq=None)
            else:
                if self.data.env == "all":
                    query_set = Case.objects.filter(
                        Q(case_type__in=self.data.group), Q(case_seq=None)
                    )
                else:
                    query_set = Case.objects.filter(
                        Q(case_type__in=self.data.group),
                        Q(case_env__in=["general", self.data.env]),
                        Q(case_seq=None),
                    )
            return len(json.loads(serializers.serialize("json", query_set)))


if __name__ == "__main__":
    # pool.submit(Executor().executor())
    logger.debug(logger)
