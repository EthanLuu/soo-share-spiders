from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from msedge.selenium_tools import Edge, EdgeOptions
import time
# 引入 ActionChains 类
from selenium.webdriver.common.action_chains import ActionChains
from config import Config
import requests

# options = EdgeOptions()
# options.use_chromium = True
# options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"  # 浏览器的位置
# driver = Edge(
#     options=options,
#     executable_path=r"C:\Projects\lib\msedgedriver.exe")  # 相应的浏览器的驱动位置

driver = webdriver.Chrome(executable_path=Config.chrome_path)

# 登录
driver.get("https://visa.vfsglobal.com/chn/zh/che/login")

time.sleep(5)

# 等待登录框出现
element = WebDriverWait(driver, 5, 0.5).until(
    EC.presence_of_element_located((By.ID, "mat-input-0")))
driver.find_element_by_id("mat-input-0").send_keys(Config.vfs_user_name)
password_input = driver.find_element_by_id("mat-input-1").send_keys(
    Config.vfs_user_name)

button = driver.find_element_by_class_name("btn-brand-orange")
button.click()

# 等待预约管理出现
element = WebDriverWait(driver, 20, 0.5).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR,
         ".c-brand-orange.text-decoration-underline.cursor-pointer")))
element.click()

time.sleep(5)
# 打开预约详情
element = WebDriverWait(driver, 20, 0.5).until(
    EC.presence_of_element_located((By.ID, "mat-expansion-panel-header-1")))
actions = ActionChains(driver)
actions.move_to_element(element).click().perform()

# 重新预约
time.sleep(5)
element = WebDriverWait(driver, 20, 0.5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".fa-clock-o")))
actions = ActionChains(driver)
actions.move_to_element(element).click().perform()

# 看看周五
element = WebDriverWait(driver, 20, 0.5).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, '[data-date="2023-08-11"]')))
class_name = element.get_attribute("class")
print(class_name)

# 下一页
time.sleep(5)
button = driver.find_element_by_css_selector(".fc-next-button")
actions = ActionChains(driver)
actions.move_to_element(element).click().perform()

# 找到有效日期
element = WebDriverWait(driver, 20, 0.5).until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, '[data-date="2023-09-15"]')))
class_name = element.get_attribute("class")
print(class_name)

title = "签证空闲日期提醒"
content = "8/11"
requests.get(Config.push_plus_url + "&title=" + title + "&content=" + content)