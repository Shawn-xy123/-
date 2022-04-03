# Health_System_Auto_Daily_Check_in
中科大健康系统要求每日打开，模拟浏览器端自动打卡
分别是火狐浏览器和谷歌浏览器，火狐浏览器不需要输入验证码，比较简单。而谷歌浏览器需要输入验证码，为此申请了百度智能云的数字识别API来识别验证码
，之后只需要填写学号姓名和申请到的API相关信息，挂在服务器上跑即可。

具体步骤请参考本人博客https://blog.csdn.net/qq_44140780/article/details/123459767?spm=1001.2014.3001.5501


@[TOC](文章目录)

---

# 前言

学校很烦，申请回校必须连续14天在系统上打卡后才能申请，但是自己有时候要忘记，所以写了一个自动打卡的代码挂在服务器上跑，每天定时打卡。所采用的是python第三方库selenium模拟谷歌浏览器来实现，其中会遇到验证码识别的问题，采用百度智能云的API函数来识别。


---


# 一、下载需要的python第三方库

## 1.Selenium

安装：`pip install selenium`

selenium是一个强大的基于浏览器的开源自动化测试工具。支持的浏览器包括IE、Chrome和Firefox等。
我们需要下载浏览器驱动，这里用的是Google浏览器驱动
Google浏览器驱动：[官网地址](https://sites.google.com/a/chromium.org/chromedriver/home)

选择适配的浏览器版本和系统，然后将下载得到的文件放到python文件的同目录下。

## 2.Baidu_aip

安装：`pip install baidu_aip`

baidu_aip是百度文字识别的OCR（Optical Character Recognition，光学字符识别）。我用这个库来调用百度智能云的API函数从而来识别登录时所需的验证码。


## 3.Pillow

安装：`pip install pillow`

pillow库是python最常用的第三方图像处理库,用来处理网页上截取的验证码图片。

---

# 二、申请百度智能云API函数

## 1.登录百度智能云

百度智能云:[官网](https://cloud.baidu.com/?_=1643866413132)

若没有账号请自行注册。
		

## 2.申请项目接口函数

登录后选择 产品 $\rightarrow$人工智能$\rightarrow$通用场景文字识别
![点击产品服务](https://img-blog.csdnimg.cn/8ea98bc307ab45818766a65d640a1348.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA54Gr54iG55qE5bCP5riF5paw,size_20,color_FFFFFF,t_70,g_se,x_16)
点击使用，填好个人信息后提交，提交后转到以下界面:
![在这里插入图片描述](https://img-blog.csdnimg.cn/14485a6a74564ff6a0beaa7b63f86483.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA54Gr54iG55qE5bCP5riF5paw,size_20,color_FFFFFF,t_70,g_se,x_16)
若未跳转则再重复上述操作，到服务中去找文字识别，使用即可。
点击右下角领取免费资源，填写信息，0元领取后，点击创建应用：
![在这里插入图片描述](https://img-blog.csdnimg.cn/8978bc024bf24b2c999750887550bf9e.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA54Gr54iG55qE5bCP5riF5paw,size_20,color_FFFFFF,t_70,g_se,x_16)
填写各种信息，点击创建
![在这里插入图片描述](https://img-blog.csdnimg.cn/a7805c6128f743d8b771bd1b97c1db15.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA54Gr54iG55qE5bCP5riF5paw,size_20,color_FFFFFF,t_70,g_se,x_16)
查看应用详情：
![在这里插入图片描述](https://img-blog.csdnimg.cn/2828bb9ae1aa4d0eaa6d9394adad1f36.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA54Gr54iG55qE5bCP5riF5paw,size_20,color_FFFFFF,t_70,g_se,x_16)
后续会用到红色方框中的内容

---

# 三、代码实现

## 1.导入三方库

````python
from selenium import webdriver
from PIL import Image
from aip import AipOcr
import time
````

## 2.验证码获取和处理

### 1.连接网址获取登录验证码


```python
browser=webdriver.Chrome(executable_path='chromedriver.exe')
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

```

其中find_element_by_xpath()函数根据xpath来定位位置
![在这里插入图片描述](https://img-blog.csdnimg.cn/16ebbd29ee8c4d5aa2620b535db73ed0.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA54Gr54iG55qE5bCP5riF5paw,size_20,color_FFFFFF,t_70,g_se,x_16)
浏览器按F12定位验证码图片后，复制XPath即可。之后将截取的验证码图片转化为灰度图再二值化，效果如下:
原图:
![在这里插入图片描述](https://img-blog.csdnimg.cn/b65326172b7b4eaf9e9bb309ffdbe0b7.png)
转化后:
![在这里插入图片描述](https://img-blog.csdnimg.cn/72c7cd8a684a43e1b7b61b769b612f1a.png)

### 2.识别验证码

```python
def identify_validation_code():

    APP_ID=
    API_key=
    SECRET_KEY=
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
```

在该函数中填入之前在百度智能云申请的API接口的AppID、API Key、Secret Key后则可利用API函数识别刚刚保存的验证码图片，返回识别结果。

## 3.登录打卡

```python
def log_in_attendence(result):
#log in
    browser.find_element_by_xpath('//*[@id="username"]').send_keys(学号)
    browser.find_element_by_xpath('//*[@id="password"]').send_keys(密码)
    browser.find_element_by_xpath('//*[@id="validate"]').send_keys(result)
    browser.find_element_by_xpath('//*[@id="login"]').click()

    #loading,waiting 3s
    time.sleep(3)
    #attendence
    browser.find_element_by_xpath('//*[@id="report-submit-btn-a24"]').click()
    browser.close()
```

输入账号、密码、验证码后，点击登录即可，所用方法仍然
是XPath定位。登录后，利用定位，直接点击确认上报即可:
![在这里插入图片描述](https://img-blog.csdnimg.cn/fe154c52df784e099580c8be84af8ee7.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBA54Gr54iG55qE5bCP5riF5paw,size_20,color_FFFFFF,t_70,g_se,x_16)
即上述log_in_attendence函数中的:

```python
browser.find_element_by_xpath('//*[@id="report-submit-btn-a24"]').click()
```

主要程序为:

```python
if __name__=='__main__':
    while True:
        get_validatioin_image()
        result=identify_validation_code()
        # print(result)
        log_in_attendence(result)
        time.sleep(60*60*8)
```

其中定时为每8个小时打一次卡，到此只需将程序和谷歌浏览器驱动(注意服务器系统，若是Linux则需用Linux版本的驱动)上传到服务器运行即可。


---

# 总结

以上就是今天要讲的内容，本文介绍了利用python如何实现网页上自动打卡的功能。

完整代码链接:[https://github.com/Shawn-xy123/Health_System_Auto_Daily_Check_in](https://github.com/Shawn-xy123/Health_System_Auto_Daily_Check_in)
参考文章:
	[python实现网站的自动登录](https://blog.csdn.net/Paramete/article/details/103318162)


