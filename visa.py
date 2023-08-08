import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
# 引入 ActionChains 类
from selenium.webdriver.common.action_chains import ActionChains
from config import Config
from datetime import datetime

driver = webdriver.ChromiumEdge()  # 创建Chrome对象时传入参数
driver.maximize_window()


def check():
    try:
        def wait_load():
            WebDriverWait(driver, 20, 0.5).until_not(
                EC.visibility_of_element_located(
                    (By.TAG_NAME, "ngx-ui-loader")))

        # 登录
        driver.get("https://visa.vfsglobal.com/chn/zh/che/login")

        time.sleep(5)
        # 等待登录框出现
        element = WebDriverWait(driver, 20, 0.5).until(
            EC.presence_of_element_located((By.ID, "mat-input-0")))
        driver.find_element(By.ID,
                            "mat-input-0").send_keys(Config.vfs_user_name)
        driver.find_element(By.ID,
                            "mat-input-1").send_keys(Config.vfs_password)
        # 登录
        button = driver.find_element(By.CLASS_NAME, "btn-brand-orange")
        button.click()

        actions = ActionChains(driver)

        while True:
            # 点击预约管理
            time.sleep(3)
            element = WebDriverWait(driver, 20, 0.5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     ".c-brand-orange.text-decoration-underline.cursor-pointer"
                     )))
            element.click()

            # 展开预约详情
            time.sleep(4)
            element = WebDriverWait(driver, 20, 0.5).until(
                EC.presence_of_element_located((By.ID, "mat-expansion-panel-header-1")))
            actions.move_to_element(element).click().perform()

            # 重新预约
            time.sleep(3)
            element = WebDriverWait(driver, 20, 0.5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".fa-clock-o")))
            actions.move_to_element(element).click().perform()

            # 查看周五
            time.sleep(8)
            element = WebDriverWait(driver, 20, 0.5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '[data-date="2023-08-11"]')))
            class_name = element.get_attribute("class")

            title = "签证预约可用"
            if class_name.find("date-availiable") >= 0:
                print('Wechat sent')
                requests.get(Config.server_url + "title=" + title)
            else:
                print("Friday Not Available")

            # 看看可预约日期
            valids = []
            for i in range(10, 30):
                element = driver.find_element(
                    By.CSS_SELECTOR, f'[data-date="2023-08-{str(i)}"]')
                class_name = element.get_attribute("class")
                if (class_name.find("date-availiable") >= 0):
                    valids.append(i)

            cur = datetime.now()
            formatted_time = cur.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{formatted_time} 有效日期：{str(valids)}")

            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            break
            # 返回个人中心
            button = driver.find_element(By.CLASS_NAME,
                                         "btn-outline-brand-orange")
            actions.move_to_element(button).click().perform()
    except Exception as e:
        print("发生了一个异常:", str(e))
        driver.quit()


while True:
    try:
        check()
    except:
        time.sleep(30)