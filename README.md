**从任何平台过来的朋友们请先阅读此说明（除了下方的英文）！**

**This is a project for someone who wants to send morning greeting to his/her girlfriend/boyfriend but without programming experience. It's just a simple python script taking advantage of Wechat Official Test Platform. It may be useless for people outside China. Please ignore this project if you are not using Wechat or you are a programmer.**

# 每日早安推送

基于[rxrw/daily_morning(每日早安推送给别人家的女朋友)](https://github.com/rxrw/daily_morning)修改而来，更改了配置文件读取方式和添加了课程表的功能

由于更改了配置文件的读取方式，github actions 不可用于部署此项目，可用于服务器或24小时不断电不断网的电脑，因此单独保留为我自己的玩具项目

## 使用说明

效果如图。当然，文字是可以修改的。

<img src="https://user-images.githubusercontent.com/75666185/188603431-c5ecc39e-7c70-48c4-a00b-a72b62644a8d.jpg" width=300px/>

首先，按图搜索，测试号，进来之后微信扫码登录！

![cf7dbd4502df44765ed3506f55caea5](https://user-images.githubusercontent.com/9566402/183242272-134e37e7-718d-42dd-9ed7-fca2810e94e6.png)


按下图，创建模板，设置变量，把微信公众平台上的各种字符串按说明创建,在嵌套括号里填入变量，变量末尾必须要带.DATA

![71bf9d11a876d23ef0f0728645a8ba0](https://user-images.githubusercontent.com/9566402/183242301-fd6ab30e-bfe5-4245-b2a9-f690184db307.png)
![381e8ee4a7c5ec6b8c09719f2c7e486](https://user-images.githubusercontent.com/9566402/183242295-4dcf06bb-2083-4883-8745-0af753ca805c.png)


文字来一遍

APP_ID: 公众平台 appID

APP_SECRET: 公众平台 appSecret

TEMPLATE_ID: 模板 ID

USER_ID: 接收人的 OpenID 多个用换行分隔

START_DATE: 正数日期，格式：2008-08-08

CITY: 城市，不要加市，准确到地级市。比如：北京、天津、广州、承德。

TIMETABLE: 今天的课程，需要配置文件中按注释要求配置启用

列出所有变量的公众号模板如下

```
今天是{{date.DATA}},{{week_day.DATA}} 
我们已经相爱{{love_days.DATA}}天
天气：{{weather.DATA}} 
温度：{{highest.DATA}}---{{lowest.DATA}} 
湿度：{{humidity.DATA}} 
风力：{{wind.DATA}} 
空气质量：{{air_quality.DATA}} 指数：{{air_data.DATA}} 

{{words.DATA}}

{{timetable.DATA}}
```


启用后可以直接运行，看看女朋友的手机有没有收到推送吧！
这个定时任务是每天早晨7点推送，如果会编程的同学可以自己自定义一些东西～

图中的操作，除了各种英文字符串不一样，模板消息中的中文不一样，其他的应该都是一样的，不然程序跑不通的


ps. 有一些注意事项在此补充

1. 第一次登录微信公众平台测试号给的 app secret 是错误的，刷新一下页面即可
2. 生日的日期格式是：`05-20`，纪念日的格式是 `2022-08-09`，请注意区分。城市请写到地级市，比如：`北京`，`广州`，`承德`
3. 变量中粘贴的各种英文字符串不要有空格，不要有换行，除了模板之外都没有换行

## 代码使用
如果你有一个自己的服务器，或是不会关机的电脑，可以通过如下方式使用代码。本项目使用Python3且建议使用环境管理工具设置单独环境。


1. 首先clone本仓库：

```bash
git clone https://github.com/ink-soul/daily_morning.git
```

2. 安装依赖：

```bash
cd daily_morning

pip3 install -r requirements.txt
```

3. 根据示例完成配置文件`config.yaml`。 `app_id`、 `app_secret`、 `user_ids` 和 `template_id` 的配置可参考[使用说明](#使用说明)

4. 运行代码`timer.py`，即可实现每日定时发送：

```bash
python3 timer.py
```


## 版权相关


 **本项目遵循 [GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt) 协议：凡使用本项目，其代码必须公开；如由此项目衍生的收费服务，必须提前告知终端用户此项目是可以免费获得及收费的理由；在本项目基础上 Fork、修改后的代码，必须采用 GPLv3 协议。此协议受全世界版权法律保护，本人保留对一切违反本协议行为诉诸法律的权力。**

