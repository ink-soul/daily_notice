from datetime import date, datetime, timedelta
import math
from wechatpy import WeChatClient, WeChatClientException
from wechatpy.client.api import WeChatMessage
import requests
import random
import re
import yaml


import timetable


with open("config.yaml", "r", encoding="utf-8") as fd:
  config = yaml.load(fd,Loader=yaml.FullLoader)

config['USER_ID'] = '\n'.join(config['USER_ID'])

if type(config['BIRTHDAY']) is list:    
  config['BIRTHDAY'] = '\n'.join(config['BIRTHDAY'])
else:
  config['BIRTHDAY'] = config['BIRTHDAY']


nowtime = datetime.utcnow() + timedelta(hours=8)  # 东八区时间
today = datetime.strptime(str(nowtime.date()), "%Y-%m-%d") #今天的日期

start_date = config['START_DATE']
city = config['CITY']
birthday = config['BIRTHDAY']

app_id = config['APP_ID']
app_secret = config['APP_SECRET']

user_ids = config['USER_ID'].split("\n")

template_id = config['TEMPLATE_ID']

timetable_enabled = config['TIMETABLE_ENABLED']
if timetable_enabled == True :
  total_number_of_weeks = config['TOTAL_NUMBER_OF_WEEKS']
  start_date_of_this_semester = config['START_DATE_OF_THIS_SEMESTER']
  words_no_class_today = config['WORDS_NO_CLASS_TODAY']
else:
  total_number_of_weeks=start_date_of_this_semester = words_no_class_today = None

fd.close()

if app_id is None or app_secret is None:
  print('请设置 APP_ID 和 APP_SECRET')
  exit(422)

if not user_ids:
  print('请设置 USER_ID，若存在多个 ID 用回车分开')
  exit(422)

if template_id is None:
  print('请设置 TEMPLATE_ID')
  exit(422)

# weather 直接返回对象，在使用的地方用字段进行调用。
def get_weather():
  if city is None:
    print('请设置城市')
    return None
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  # OpenRefactory Warning: The 'requests.get' method does not use any 'timeout' threshold which may cause program to hang indefinitely.
  res = requests.get(url, timeout=100).json()
  if res is None:
    return None
  if res['code'] != 0:
    return None
  weather = res['data']['list'][0]
  return weather

# 获取当前日期为星期几
def get_week_day():
  week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
  week_day = week_list[datetime.date(today).weekday()]
  return week_day

# 纪念日正数
def get_memorial_days_count():
  if start_date is None:
    print('没有设置 START_DATE')
    return 0
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

# 各种倒计时
def get_counter_left(aim_date):
  if aim_date is None:
    return 0

  # 为了经常填错日期的同学们
  if re.match(r'^\d{1,2}\-\d{1,2}$', aim_date):
    next = datetime.strptime(str(date.today().year) + "-" + aim_date, "%Y-%m-%d")
  elif re.match(r'^\d{2,4}\-\d{1,2}\-\d{1,2}$', aim_date):
    next = datetime.strptime(aim_date, "%Y-%m-%d")
    next = next.replace(nowtime.year)
  else:
    print('日期格式不符合要求')
    
  if next < nowtime:
    next = next.replace(year=next.year + 1)
  return (next - today).days


# 彩虹屁 接口不稳定，所以失败的话会重新调用，直到成功
def get_words():
  # OpenRefactory Warning: The 'requests.get' method does not use any 'timeout' threshold which may cause program to hang indefinitely.
  words = requests.get("https://api.shadiao.pro/chp", timeout=100)
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def format_temperature(temperature):
  return math.floor(temperature)

# 随机颜色
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

# 返回一个数组，循环产生变量
def split_birthday():
  if birthday is None:
    return None
  return birthday.split('\n')


weather = get_weather()
if weather is None:
  print('获取天气失败')
  exit(422)

# 要发送的数据结构体
data = {
  "city": {
    "value": city,
    "color": get_random_color()
  },
  "date": {
    "value": today.strftime('%Y年%m月%d日'),
    "color": get_random_color()
  },
  "week_day": {
    "value": get_week_day(),
    "color": get_random_color()
  },
  "weather": {
    "value": weather['weather'],
    "color": get_random_color()
  },
  "humidity": {
    "value": weather['humidity'],
    "color": get_random_color()
  },
  "wind": {
    "value": weather['wind'],
    "color": get_random_color()
  },
  "air_data": {
    "value": weather['airData'],
    "color": get_random_color()
  },
  "air_quality": {
    "value": weather['airQuality'],
    "color": get_random_color()
  },
  "temperature": {
    "value": math.floor(weather['temp']),
    "color": get_random_color()
  },
  "highest": {
    "value": math.floor(weather['high']),
    "color": get_random_color()
  },
  "lowest": {
    "value": math.floor(weather['low']),
    "color": get_random_color()
  },
  "love_days": {
    "value": get_memorial_days_count(),
    "color": get_random_color()
  },
  "words": {
    "value": get_words(),
    "color": get_random_color()
  },
  "timetable":{
    "value": timetable.get_classes_today(timetable_enabled,words_no_class_today,nowtime,today,start_date_of_this_semester),
    "color": get_random_color()
  },
}

for index, aim_date in enumerate(split_birthday()):
  key_name = "birthday_left"
  if index != 0:
    key_name = key_name + "_%d" % index
  data[key_name] = {
    "value": get_counter_left(aim_date),
    "color": get_random_color()
  }

if __name__ == '__main__':
  try:
    client = WeChatClient(app_id, app_secret)
  except WeChatClientException as e:
    print('微信获取 token 失败，请检查 APP_ID 和 APP_SECRET，或当日调用量是否已达到微信限制。')
    exit(502)

  wm = WeChatMessage(client)
  count = 0
  try:
    for user_id in user_ids:
      print('正在发送给 %s, 数据如下：%s' % (user_id, data))
      res = wm.send_template(user_id, template_id, data)
      count+=1
  except WeChatClientException as e:
    print('微信端返回错误：%s。错误代码：%d' % (e.errmsg, e.errcode))
    exit(502)

  print("发送了" + str(count) + "条消息")
