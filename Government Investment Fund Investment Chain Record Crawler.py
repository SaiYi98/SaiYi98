


# 爬取所投资项目链条
# 运行前需先使用cmd键入chromedriver并回车，呼出chromedriver

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException 
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

import time
import random
import json

options = Options()

driver = webdriver.Chrome()

# 选择保存文件的目录
output_folder = r'C:\Users\GF-DATA\Desktop\test\\'

url = 'https://max.pedata.cn/client/lp/list'

driver.get(url)

input("Press Enter after you have logged in...")

# 保存登录后的cookies
cookies = driver.get_cookies()
with open("cookies.txt", 'w') as file:
    json.dump(cookies, file)

# 加载 cookies
with open("cookies.txt", 'r') as file:
    cookies = json.load(file)
for cookie in cookies:
    driver.add_cookie(cookie)

driver.get(url)

# 设置隐式等待时间
driver.implicitly_wait(3)

# 在保存页面HTML之前，找到并点击'进阶筛选项'链接
advanced_filter = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div[2]/a[2]')
advanced_filter.click()

# 需要手动按筛选标签 - 政府引导基金 - 电子信息产业
input("请手动完成筛选然后按回车键继续...")

page_num = 33
time.sleep(3)

while True:
    # 保存页面HTML
    with open(f'{output_folder}page_{page_num}.html', 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    
    # 获取所有数据链接并依次点击

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 
                            '//*[@id="maxTable"]/div[1]/div/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[1]/div/div/div[2]/a')))
    data_links = driver.find_elements_by_xpath(
        '//*[@id="maxTable"]/div[1]/div/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[1]/div/div/div[2]/a')


#     data_links = driver.find_elements_by_xpath('//*[@id="maxTable"]/div[1]/div/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[1]/div/div/div[2]/a')
#     print(data_links)
    
    for i, link in enumerate(data_links, 1):
        try:
            url = link.get_attribute('href')  # 获取链接的 href 属性
            driver.execute_script(f'window.open("{url}","_blank");')  # 在新的标签页中打开链接
            driver.switch_to.window(driver.window_handles[-1])  # 切换到新的标签页
            
            try:
                # 点击 '投资项目'
                wait = WebDriverWait(driver, 10) # 等待最多10秒
                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div[1]/div[4]')))
                time.sleep(3)
                element.click()

                # 点击 '所投基金投资项目'
                wait = WebDriverWait(driver, 10) # 等待最多10秒
                fund_invest_project = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/div/div[2]/div/div[3]/div[5]/div[2]/div[2]/div[1]/div/div/div/div/div[1]/div[3]')))
                time.sleep(3)
                fund_invest_project.click()

            except TimeoutException:
                print("发生了 TimeoutException，回到主数据库")
                driver.close()  # 关闭新的标签页
                driver.switch_to.window(driver.window_handles[0])  # 切换回原始窗口
                continue
            # 点击 '投资项目'
#             wait = WebDriverWait(driver, 10)  # 等待最多10秒
#             element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/div/div[2]/div/div[1]/div/div/div/div/div[1]/div[5]')))
#             time.sleep(3)
#             element.click()

#             # 点击 '所投基金投资项目'
#             wait = WebDriverWait(driver, 10)  # 等待最多10秒
#             fund_invest_project = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/div/div[2]/div/div[3]/div[5]/div[2]/div[2]/div[1]/div/div/div/div/div[1]/div[3]')))
#             time.sleep(3)
#             fund_invest_project.click()
        
            try:
                # 尝试查找并点击下拉菜单
                dropdown_menu_link = driver.find_element_by_xpath('//*[@id="app"]/div/div/div/div/div[2]/div/div[3]/div[5]/div[2]/div[2]/div[3]/div[3]/div[2]/div[1]/div[2]/i')
                dropdown_menu_link.click()
                time.sleep(3)  # 等待下拉菜单加载完成
            except NoSuchElementException:
                pass  # 下拉菜单不存在，不做任何事情，直接尝试查找 '电子信息产业' 标签

            try:
                # 查找所有包含特定属性的 span 元素
                span_elements = driver.find_elements_by_css_selector("span[data-v-a4d4bae8]")

                for span in span_elements:
                    if "电子信息产业" in span.text:
                        span.click()
                        break
            except NoSuchElementException:
                # '电子信息产业'选项不存在，关闭页面并继续下一个循环
                driver.close()  # 关闭新的标签页
                driver.switch_to.window(driver.window_handles[0])  # 切换回原始窗口
                continue

            # 开始处理子数据库的每一页
            sub_page_num = 1
            while True:
                # 保存子数据库页面的 HTML
                with open(f'{output_folder}subpage_{page_num}_{i}_{sub_page_num}.mhtml', 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                time.sleep(2)
                
                # 在这个新页面中获取所有的按钮
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div/div[2]/div/div[3]/div[5]/div[2]/div[2]/div[3]/div[3]/div[4]/div/div/div[1]/div[2]/div[1]/div[2]/table/tbody/tr/td[2]/div/div')))
                    button_links = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div/div/div[2]/div/div[3]/div[5]/div[2]/div[2]/div[3]/div[3]/div[4]/div/div/div[1]/div[2]/div[1]/div[2]/table/tbody/tr/td[2]/div/div')
                except TimeoutException:
                    print("所投基金无项目,关闭标签并返回母数据库")
                    break
                
                # 遍历所有的按钮并依次点击
                time.sleep(2)
                for j, button in enumerate(button_links, 1):
                    try:
                        time.sleep(1)
                        # 点击按钮
                        button.click()

                        # 等待弹出窗口加载完成，保存弹出窗口的 HTML
                        time.sleep(2)
                        with open(f'{output_folder}popup_{page_num}_{i}_{sub_page_num}_{j}.mhtml', 'w', encoding='utf-8') as f:
                            f.write(driver.page_source)

                        # 关闭弹出窗口
                        close_button_xpath = '/html/body/div[2]/div/div[2]/div/div[2]/div[3]/div/button' 
                        close_button = driver.find_element_by_xpath(close_button_xpath)
                        close_button.click()
                        time.sleep(1) # 等待窗口关闭
                    except NoSuchElementException:
                        print(f"第 {page_num} 页，第 {i} 行，第 {j} 个按钮不存在")
                        continue
                
                # 查找并点击子数据库的下一页按钮
                time.sleep(2)
                next_sub_page_button = None
                next_sub_page_button_candidates = driver.find_elements_by_xpath("//a[contains(text(),'下一页')]")

                # 如果 '下一页' 按钮不存在，跳出循环
                if not next_sub_page_button_candidates:
                    print("下一页按钮不存在，关闭标签页并回到母数据库")
#                    driver.close()  # 关闭新的标签页
#                    driver.switch_to.window(driver.window_handles[0])  # 切换回原始窗口
                    break

                for candidate in next_sub_page_button_candidates:
                    try:
                        # 检查候选按钮是否在可视区域内
                        if candidate.is_displayed():
                            next_sub_page_button = candidate
                            break
                    except StaleElementReferenceException:
                        continue  # 如果元素过时，那么跳过这个元素
                
                # 如果在可视区域内找不到 '下一页' 按钮，跳出循环
                if next_sub_page_button is None:
                    print("可视区域内找不到下一页按钮，关闭标签页并回到母数据库")
#                    driver.close()  # 关闭新的标签页
#                    driver.switch_to.window(driver.window_handles[0])  # 切换回原始窗口
                    break

                try:
                    # 检查 "下一页" 按钮的 class 或 aria-disabled 属性
                    parent_li = next_sub_page_button.find_element_by_xpath("..")
                    if 'ant-pagination-disabled' in parent_li.get_attribute("class") or parent_li.get_attribute("aria-disabled") == "true":
                        print(f"已经到达子数据库 {page_num}_{i} 的最后一页")
                        break
                except StaleElementReferenceException as e:
                    print("元素已过期，关闭标签页并回到母数据库")
#                    driver.close()  # 关闭新的标签页
#                    driver.switch_to.window(driver.window_handles[0])  # 切换回原始窗口
                    break

                # 使用 ActionChains 来模拟鼠标操作点击按钮
                actions = ActionChains(driver)
                actions.move_to_element(next_sub_page_button).click().perform()
#                 print('点了')
                sub_page_num += 1
                time.sleep(2)

        # 捕获 NoSuchElementException 异常
        except NoSuchElementException as e:
            print(f"元素未找到: {e}")
#            driver.close()  # 关闭新的标签页
#            driver.switch_to.window(driver.window_handles[0])  # 切换回原始窗口
            continue
        
        driver.close()  # 关闭新的标签页
        driver.switch_to.window(driver.window_handles[0])  # 切换回原始窗口

        # 主数据库翻页
    try:
        time.sleep(2)
        # 滚动到页面最下方
        scrollable_div = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]')
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scrollable_div)
        print('翻了')
        
        # 查找并点击下一页按钮
        next_page_button = None
        next_page_button_candidates = driver.find_elements_by_xpath("//a[contains(text(),'下一页')]")
        print('点了')
        
        for candidate in next_page_button_candidates:
            # 检查候选按钮是否在可视区域内
            if candidate.is_displayed():
                next_page_button = candidate
                break

        # 检查 "下一页" 按钮的 class 或 aria-disabled 属性
        parent_li = next_page_button.find_element_by_xpath("..")
        if 'ant-pagination-disabled' in parent_li.get_attribute("class") or parent_li.get_attribute("aria-disabled") == "true":
            print("已经到达最后一页")
            break

        # 使用 ActionChains 来模拟鼠标操作点击按钮
        actions = ActionChains(driver)
        actions.move_to_element(next_page_button).click().perform()

    except NoSuchElementException as e:
        print(f"元素未找到: {e}")
        break

    page_num += 1
    time.sleep(3)

driver.quit()


# In[ ]:




