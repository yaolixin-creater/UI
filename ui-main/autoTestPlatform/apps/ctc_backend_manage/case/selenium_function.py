import datetime
import json
import os
import sys
import time
import logging
import random
import string

# 导入webdriver
from selenium import webdriver

# 导入异常类
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 导入By类
from selenium.webdriver.common.by import By

# 导入chrome配置
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# 导入期望场景类
from selenium.webdriver.support import expected_conditions as EC

# 导入显示等待类
from selenium.webdriver.support.ui import WebDriverWait

# 导入鼠标事件
from selenium.webdriver.common.action_chains import ActionChains
from addict import Dict

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoTestPlatform.settings")

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(PATH)

logger = logging.getLogger("autotest")
""" 
    非共性的操作要素映射表，这个表主要由操作类引用的要素决定，
    主要取决于操作方法中定义的key,
    如果操作类中的方法需要引入非共性的要素key，
    请定义在这个字典中，
    前端会读取这个非共性要素映射表，将Key值动态渲染到页面上，
    以便任何人配置  
"""
operation_map = {
    "click": [],
    "mouse_click": [],
    "mask_layer_disappear": [],
    "clear": [],
    "input": [],
    "switch_to_childframe": [],
    "switch_to_parentframe": [],
    "input_into_searchbox": [],
    "assert_wait_response": [],
    "assert_find_text": [],
    "assert_find_element": [],
    "scroll_window_bottom": [],
    "scroll_window_top": [],
    "compulsively_wait": [],
    "select_only_by_id": [],
    "execute_script_by_element": [],
    "execute_script": [],
    "operate_date_only_by_id": [],
    "open_new_window": [],
    "get_url": [],
    "refresh_get_url": [],
    "close_window": [],
    "obviously_wait": [],
    "get_element": [],
    "banckend_menu_scroll": []
}


class SeleniumFunction:
    def __init__(self, instance_browser=True):
        # Chromdriver 的启动项
        if instance_browser:
            options = webdriver.ChromeOptions()
            options.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')
            # options.add_argument("--headless")
            # options.add_argument('--no-sandbox')
            options.add_experimental_option("w3c", False)
            # options.add_argument('--disable-gpu') #禁用gpu，一般生产环境会使用，因为服务器大多没有gpu
            # options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
            options.add_experimental_option("excludeSwitches", ['enable-automation'])
            options.add_experimental_option('perfLoggingPrefs', {'enableNetwork': True})
            caps = DesiredCapabilities.CHROME
            caps['goog:loggingPrefs'] = {'performance': 'ALL'}

            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False
            }
            options.add_experimental_option('prefs', prefs)
            path = os.path.join(
                os.path.dirname(__file__), "Driver", "chromedriver"
                # os.path.dirname(__file__), "Driver", "chromedriver_linux_97"
            ).replace("\\", "/")
            self.driver = webdriver.Chrome(
                executable_path=path, desired_capabilities=caps, options=options
            )
            self.driver.maximize_window()

            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
              """
            })
        else:
            pass

    def scroll_window_bottom(self, obj):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.1)

    def scroll_window_top(self, obj):
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.1)

    def banckend_menu_scroll(self, obj):
        js = f'document.querySelector("body > div.layout > div.dao-nav-menu > div.menus").scrollTop = {str(obj["action_value"])}'
        print(js)
        self.driver.execute_script(js)
        time.sleep(0.1)

    def get_url(self, obj):
        """
        访问地址，行为参数：访问的地址 """
        import requests

        action_value = obj["action_value"]
        try:
            # requests.get(action_value)
            # logger.debug("后端服务正常。。。")
            pass
        except Exception as e:
            raise Exception("后端服务异常，无法打开页面；\n{}".format(str(e)))
        self.driver.get(action_value)

    def refresh_get_url(self, obj, host):
        try:
            action_value = obj["action_value"]
            action_value = str(action_value).replace("{host}", host)
            logger.info("*" * 50)
            logger.info(action_value)
            self.driver.get(action_value)
            logger.info("执行步骤【({}){}】成功...".format(obj.step_seq, obj.action_desc))
        except Exception as e:
            err_msg = "执行步骤【({}){}】失败...".format(obj.step_seq, obj.action_desc)
            logger.info(err_msg)
            import traceback

            traceback.print_exc()
            raise Exception("{}; {}".format(err_msg, str(e)))

    def get_element(self, obj):
        """
        获取元素，行为参数：不接受参数（内部调用） """
        element = self.obviously_wait(obj)
        pre_style = element.value_of_css_property('border')
        self.driver.execute_script('arguments[0].style.border="2px solid red";', element)
        time.sleep(1)
        self.driver.execute_script(f'arguments[0].style.border="{pre_style}";', element)
        return element

    def mouse_click(self, obj):
        ActionChains(self.driver).move_to_element(
            self.get_element(obj)
        ).click().perform()

    def click(self, obj):
        """
        点击元素，行为参数：不接受参数 """
        self.get_element(obj).click()

    def mask_layer_disappear(self, obj):
        self.disappear(obj)

    def clear(self, obj):
        """
        清空内容，行为参数：不接受参数 """
        self.get_element(obj).clear()

    def input(self, obj):
        """
        输入内容，行为参数：输入文本框的内容 """
        action_value = obj["action_value"]
        if action_value == "{random_str}":
            random_value = ''.join(random.sample(string.ascii_letters + string.digits, 4))
            action_value = "auto" + random_value
        self.get_element(obj).send_keys(action_value)

    def obviously_wait(self, obj, timeout=10):
        """
        显式等待，行为参数：不接受参数（一般不用）
        fuck, only capture timeout exception,
        need declare exeption self """
        obj = Dict(obj)
        try:
            return WebDriverWait(self.driver, timeout).until(
                # 元素可见，可点击
                EC.element_to_be_clickable(
                    # EC.presence_of_element_located(
                    (getattr(By, obj.loc_type.upper().replace(" ", "_")), obj.loc_value)
                )
            )
        # except NoSuchElementException:
        #     raise Exception('根据loc_value未定位到元素...')
        except TimeoutException:
            raise Exception("超时（原因一：元素定位值错误，原因二：页面未打开）")
        except Exception as e:
            raise Exception(str(e))

    def disappear(self, obj, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.visibility_of_element_located(
                    (getattr(By, obj.loc_type.upper().replace(" ", "_")), obj.loc_value)
                )
            )
            time.sleep(0.1)
            return True
        except TimeoutException:
            raise Exception("等待遮罩层消失，超时...")
        except Exception as e:
            raise Exception(str(e))

    def compulsively_wait(self, obj):
        """
        强制等待，行为参数：时间/s """
        action_value = obj["action_value"]
        time.sleep(int(action_value))

    def switch_to_childframe(self, obj):
        """
        切入小框，行为参数：小框编号（选填） """
        action_value = obj["action_value"]
        if action_value == "" or action_value is None:
            self.driver.switch_to.frame(0)
        else:
            self.driver.switch_to.frame(int(action_value))
        time.sleep(0.25)

    def switch_to_parentframe(self, obj):
        """ 切回原框，行为参数：不接受参数 """
        self.driver.switch_to.parent_frame()

    def select_only_by_id(self, obj):
        """
        操作下拉列表 仅根据id来定位下拉框，选择下拉框第几个元素，
        下拉列表需勾选的不能使用如下方法 """
        loc_value = obj["loc_value"]
        action_value = obj["action_value"]
        # 修改根据id定位的元素的等待情况
        obj["loc_type"] = "id"
        self.click(obj)
        select = self.driver.find_element_by_id(loc_value)
        all_options = select.find_elements_by_tag_name("option")
        all_options[int(action_value) - 1].click()

    def operate_date_only_by_id(self, obj):
        """
        操作日期表 仅根据id来定位下拉框，操作日期，
        行为参数：距离系统日期的天数差（当天为0） """
        loc_value = obj["loc_value"]
        action_value = obj["action_value"]
        js = "$('input[id=" + loc_value + "]').attr('readonly', '')"  # 4.jQuery
        self.driver.execute_script(js)
        if action_value == "0" or action_value is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            date = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime(
                "%Y-%m-%d"
            )
        logger.debug(date)
        obj["loc_type"] = "id"
        obj["action_value"] = str(date)
        self.input(obj)  # 键入日期

    def input_into_searchbox(self, obj):
        """
        搜索框强行输入文字,行为参数：输入的内容（仅支持根据id定位） """
        loc_value = obj["loc_value"]
        js = "$('input[id=" + loc_value + "]').attr('readonly', '')"  # 4.jQuery
        self.driver.execute_script(js)
        obj["loc_type"] = "id"
        self.input(obj)

    @staticmethod
    def get_HttpStatus(obj, driver):
        """
        判断点击之后触发链接的响应状态，获得响应状态，行为参数：接口地址（标识）（内部调用） """
        assert_value = obj["assert_value"]
        collected = 0
        resp_info = [None]
        for responseReceived in driver.get_log("performance"):
            logger.debug("google browser console: {}".format(responseReceived))
            try:
                response = json.loads(responseReceived["message"])["message"][
                    "params"
                ]
                if response.get("response"):
                    response = response.get("response")
                    if assert_value in str(response["url"]):
                        collected += 1
                        resp_info.append(
                            [response["status"], response["statusText"], response["url"]]
                        )
            except:
                pass
        logger.debug("collected: {}".format(collected))
        return resp_info[-1], collected, resp_info

    def assert_wait_response(self, obj):
        """
        等待查询请求加载完成，断言等待响应，行为参数：接口地址（标识）"""
        assert_value = obj["assert_value"]
        response = []

        def status():
            nonlocal response
            response, collected, resp_info = self.get_HttpStatus(obj, self.driver)
            logger.info("response get: {}".format(response))
            if response is None or response == "":
                return False
            else:
                if collected:
                    return True

        if assert_value == "nonneed":
            return ["nonneed"]
        try:
            WebDriverWait(self.driver, 60, 0.2).until(lambda x: status())
        except TimeoutException:
            raise Exception("扫描接口请求超时！浏览器控制台信息中未发现接口【{}】的请求记录".format(assert_value))
        return response

    def assert_find_text(self, obj):
        """断言某个元素的text值是否符合预期"""
        _element = self.get_element(obj)
        action_value = obj["assert_value"]
        try:
            _text = _element.text
            if _text == action_value:
                return ["nonneed"]
            else:
                return [f"预期值{action_value}和查询到的结果{_text}不一致！"]
        except Exception as e:
            raise Exception(str(e))

    def assert_find_element(self, obj):
        """断言找到某个元素"""
        _element = self.get_element(obj)
        return ["nonneed"]

    def refresh_window(self):
        """
        用例执行失败刷新 """
        self.driver.refresh()
        logger.debug("用例执行失败, 页面刷新成功...")

    def quit_window(self):
        """退出驱动并关闭所有关联的窗口"""
        self.driver.quit()

    def close_window(self, obj):
        """关闭当前窗口"""
        self.driver.close()

    def operate_all_actions(self, obj):
        """ 运行所有的动作 """
        try:
            # 找到对应的方法名并执行
            time.sleep(0.5)
            response = getattr(self, obj.ele_action)(obj)
            logger.info("执行步骤【({}){}】成功...".format(obj.step_seq, obj.action_desc))
            return response
        except Exception as e:
            err_msg = "执行步骤【({}){}】失败...".format(obj.step_seq, obj.action_desc)
            logger.info(err_msg)
            import traceback

            traceback.print_exc()
            raise Exception("{}; {}".format(err_msg, str(e)))

    def open_new_window(self, obj):
        """跳转到新窗口"""
        # 获得原始窗口句柄和所有句柄
        # current_handle = self.driver.current_window_handle
        time.sleep(1)
        all_handles = self.driver.window_handles
        # # 判断新窗口打开
        # WebDriverWait(self.driver, 10).until(EC.new_window_is_opened(all_handles))
        # 跳转到新窗口
        self.driver.switch_to.window(all_handles[-1])

    def execute_script_by_element(self, obj):
        """通过页面元素执行js脚本"""
        _element = self.get_element(obj)
        ele_action = obj["action_value"]
        self.driver.execute_script(ele_action, _element)

    def execute_script(self, obj):
        """执行js脚本"""
        self.driver.execute_script(obj["action_value"])


if __name__ == "__main__":
    # 实例化
    # sf = SeleniumFunction()
    # sf.driver.close()
    pass
