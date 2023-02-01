# coding:utf-8

import pytest
from addict import Dict
from py.xml import html
import logging
logger = logging.getLogger('autotest')


def pytest_addoption(parser):
    group = parser.getgroup('autotest')
    group.addoption(
        '--casename',
        dest='casename',
        default=[],
        action='append',
    )
    group.addoption(
        '--report_id',
        dest='report_id',
        default='',
        action='store',
    )
    group.addoption(
        '--group',
        dest='group',
        default=[],
        action='append',
    )
    group.addoption(
        '--env',
        dest='env',
        default='',
        action='store',
    )

    group.addoption(
        '--extend',
        dest='extend',
        default='',
        action='store',
    )


def pytest_collection_modifyitems(session, config, items):
    skiper = pytest.mark.skip(
        reason='SKIP',
        DONT_SHOW=True,
    )
    cases = config.getoption('casename', [])
    if len(cases) == 0:
        return
    standard_item = [
        str(item.name.split('test_all_cases[')[1].split(']')[0])
        for item in items
    ]
    special_case = [case for case in cases if case in standard_item]
    # raise Exception('special case: {}; all case: {}'.format(
    #     special_case, standard_item))
    for item in items:
        casename = item.name.split('test_all_cases[')[1].split(']')[0]
        if casename not in special_case:
            item.add_marker(skiper)
    setattr(
        config,
        'special_case',
        special_case,
    )
    if len(special_case) != len(cases):
        deprecated_case = [t for t in cases if t not in special_case]
        setattr(
            config,
            'deprecated_case',
            deprecated_case,
        )


def pytest_configure(config):
    config._metadata['BELONG_ENV'] = config.getoption('env')
    config._metadata['DESC'] = "DSP UI TEST RESULT"
    config._metadata['AUTH'] = "ALTER"


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('用例方法', class_='sortable func', col='func'))
    cells.insert(2, html.th('用例描述', class_='sortable desc', col='desc'))
    cells.insert(3, html.th('状态码', class_='sortable code', col='code'))
    cells.pop(4)


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.case_func))
    cells.insert(2, html.td(report.desc))
    cells.insert(3, html.td(report.response_code))
    cells.pop(4)


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    """ [
        '_ALLOW_MARKERS', '__class__', '__delattr__', '__dict__',
        '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
        '__getattribute__', '__gt__', '__hash__', '__init__',
        '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__',
        '__new__', '__reduce__', '__reduce_ex__', '__repr__',
        '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
        '__weakref__', '_args', '_fixtureinfo', '_getobj', '_initrequest',
        '_location', '_name2pseudofixturedef', '_nodeid', '_obj',
        '_prunetraceback', '_pyfuncitem', '_report_sections',
        '_repr_failure_py', '_request', '_skipped_by_mark', 'add_marker',
        'add_report_section', 'addfinalizer', 'callspec',
        'catch_log_handler', 'catch_log_handlers', 'cls', 'config',
        'extra_keyword_matches', 'fixturenames', 'fspath', 'funcargnames',
        'funcargs', 'function', 'get_closest_marker', 'getmodpath',
        'getparent', 'ihook', 'instance', 'iter_markers',
        'iter_markers_with_node', 'keywords', 'listchain',
        'listextrakeywords', 'listnames', 'location', 'module', 'name',
        'nextitem', 'nodeid', 'obj', 'originalname', 'own_markers',
        'parent', 'reportinfo', 'repr_failure', 'runtest', 'session',
        'setup', 'teardown', 'user_properties', 'warn'
    ] """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        report.desc = '' if item._skipped_by_mark else str(
            getattr(item.function, '__doc__'))
        report.response_code = '' if item._skipped_by_mark else str(
            getattr(item.function, '__str__'))
        report.case_func = str(report.nodeid).split('::')[2].split(
            'test_all_cases[')[1].split(']')[0]
        xfail = hasattr(report, 'wasxfail')
        import os
        filename = os.path.join(
            os.path.dirname(__file__), 'screenshot', '{}.png'.format(
                report.case_func.replace(' ',
                                         '_').replace('/',
                                                      '_').replace('\\', '_')))
        if (report.skipped and xfail) or (report.failed and not xfail):
            html = """<div><img src="/static/%s" alt="screenshot" \
                style="width:560px; height:315px;" \
                    onclick="window.open(this.src)" \
                        align="right"/></div>""" % os.path.basename(filename)
            extra.append(pytest_html.extras.html(html))
        report.extra = extra
