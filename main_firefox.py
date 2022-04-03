from selenium import webdriver
import time

while True:
    browser=webdriver.Firefox(executable_path='geckodriver')
    url = "https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin"
    browser.get(url)

    browser.find_element_by_xpath('//*[@id="username"]').send_keys(学号)
    browser.find_element_by_xpath('//*[@id="password"]').send_keys(密码)
    browser.find_element_by_xpath('//*[@id="login"]').click()

    # loading,waiting 3s
    time.sleep(3)
    # attendence
    browser.find_element_by_xpath('//*[@id="report-submit-btn-a24"]').click()
    browser.close()
    time.sleep(60*60*8)