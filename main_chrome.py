from selenium import webdriver
from PIL import Image
from aip import AipOcr
import time

#Chrome browser
#driver path : download in website https://sites.google.com/a/chromium.org/chromedriver/home
browser=webdriver.Chrome(executable_path='chromedriver.exe')

# browservim =webdriver.Firefox(executable_path='geckodriver')
#open website
def get_validatioin_image():
    url="https://passport.ustc.edu.cn/login?service=https%3A%2F%2Fweixine.ustc.edu.cn%2F2020%2Fcaslogin"
    browser.get(url)

    #find validation code
    png=browser.find_element_by_xpath('//*[@id="valiCode"]/div[2]/div/img')
    png.screenshot('capt.png')



    #process validation code image
    img=Image.open('capt.png')
    #transfer P mode to L mode
    img=img.convert('L')
    #threshhold
    count=165
    table=[]
    for i in  range(256):
        if i < count:
            table.append(0)
        else:
            table.append(1)

    img=img.point(table,'1')
    img.save('captcha1.png')



#identify validation code
#first, we need to create application in baidu intelligence cloud
#the we can get appid apikey secretkey
def identify_validation_code():

    APP_ID=***
    API_key=***
    SECRET_KEY=***
    client=AipOcr(APP_ID,API_key,SECRET_KEY)
    #read image
    def get_file_content(file_path):
        with open(file_path,'rb') as f:
            return f.read()
    image=get_file_content('captcha1.png')
    #define params
    options={'language_type':'ENG',}
    result=client.basicGeneral(image,options)
    return result['words_result'][0]['words']
    # for word in result['words_result']:
    #     captcha = (word['words'])
    #
    #     print('识别结果：' + captcha)
    #
    #     return captcha

    # return result['words_result'][0]['words'].strip()
    # for word in result['words_result']:
    #     captcha=word['words']
    #     print(captcha)

def log_in_attendence(result):
#log in
    browser.find_element_by_xpath('//*[@id="username"]').send_keys(学号)
    browser.find_element_by_xpath('//*[@id="password"]').send_keys(密码)
    # browser.find_element_by_xpath('//*[@id="validate"]').send_keys(result)
    browser.find_element_by_xpath('//*[@id="login"]').click()

    #loading,waiting 3s
    time.sleep(3)
    #attendence
    browser.find_element_by_xpath('//*[@id="report-submit-btn-a24"]').click()
    browser.close()
if __name__=='__main__':
    while True:
        # get_validatioin_image()
        # result=identify_validation_code()
        # print(result)
        result=0
        log_in_attendence(result)
        time.sleep(60*60*8)