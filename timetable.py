import math
import yaml
import re
from datetime import date, datetime
from chinese_calendar import is_holiday




#读取指定设置条目
def get_timetable_config(config_item) :
    with open("config.yaml", "r", encoding="utf-8") as fd:
        config = yaml.load(fd,Loader=yaml.FullLoader)

    timetable_config = config[config_item]

    fd.close()
    return timetable_config



# 当前学期周数
def get_num_of_week_now(nowtime,today,start_date_of_this_semester):
  
  if start_date_of_this_semester is None:
    return 0

  # 为了经常填错日期的同学们
  if re.match(r'^\d{1,2}\-\d{1,2}$', start_date_of_this_semester):
    next = datetime.strptime(str(date.today().year) + "-" + start_date_of_this_semester, "%Y-%m-%d")
  elif re.match(r'^\d{2,4}\-\d{1,2}\-\d{1,2}$', start_date_of_this_semester):
    next = datetime.strptime(start_date_of_this_semester, "%Y-%m-%d")
    next = next.replace(nowtime.year)
  else:
    print('日期格式不符合要求')
  passed_days_afrer_start_day = (today-next).days
  num_of_week_now = math.ceil(passed_days_afrer_start_day/7)
  # if next < nowtime:
  #  next = next.replace(year=next.year + 1)
  return num_of_week_now






# 根据当前日期，获取当天课表
def get_classes_today(timetable_enabled,words_no_class_today,nowtime,today,start_date_of_this_semester):
  if timetable_enabled == True :
    if is_holiday == True :
      return words_no_class_today
    week_list = ["MONDAY","TUESDAY","THIRSDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"]
    week_today = week_list[datetime.date(today).weekday()]
    class_today = get_timetable_config(week_today) 
    if class_today is None :
      return  words_no_class_today
    else :
      i = 0
      string_class_today = str(" ")
      while i < len(class_today) : # 以class_today的列表长度作为循环次数
        dick_class_today = class_today[i] # 循环次数作为列表取元素的索引
        now_num_of_week = get_num_of_week_now(nowtime,today,start_date_of_this_semester)
        # todo:将以下对比内容改写为函数
        # 单双周标志符为'1'即单周和当前周数小于结束周数且当前周数大于开始周数
        if (dick_class_today['SINGLE_BI_WEEK_MARK'] == '1' and now_num_of_week & 1 != 0) and (int(dick_class_today['END_WEEK']) >=  now_num_of_week and int(dick_class_today['START_WEEK']) <= now_num_of_week) :
          format_string = str("\n时间：{TIME}\n课程（单周）：{CLASSNAME}\n教室：{CLASSROOM}\n开始的周数：{START_WEEK}\n结束的周数：{END_WEEK}\n".format(**dick_class_today))  #格式化字符串的样式
          string_class_today =string_class_today + format_string # 格式化生成字符串，并累加
          i = i+1
        # 单双周标志符为'2'
        elif (dick_class_today['SINGLE_BI_WEEK_MARK'] == '2' and now_num_of_week & 1 == 0) and (int(dick_class_today['END_WEEK']) >=  now_num_of_week and int(dick_class_today['START_WEEK']) <= now_num_of_week) :
          format_string = str("\n时间：{TIME}\n课程（双周）：{CLASSNAME}\n教室：{CLASSROOM}\n开始的周数：{START_WEEK}\n结束的周数：{END_WEEK}\n".format(**dick_class_today))  #格式化字符串的样式
          string_class_today =string_class_today + format_string # 格式化生成字符串，并累加
          i = i+1
        # 单双周标志符为"3"即每周和当前周数小于结束周数且当前周数大于开始周数
        elif dick_class_today['SINGLE_BI_WEEK_MARK'] == '3' and (int(dick_class_today['END_WEEK']) >=  now_num_of_week and int(dick_class_today['START_WEEK']) <= now_num_of_week) :
          print(dick_class_today)
          format_string = str("\n时间：{TIME}\n课程：{CLASSNAME}\n教室：{CLASSROOM}\n开始的周数：{START_WEEK}\n结束的周数：{END_WEEK}\n".format(**dick_class_today))  #格式化字符串的样式
          string_class_today =string_class_today + format_string # 格式化生成字符串，并累加
          i = i+1
        elif now_num_of_week <= 0:
          return ("\n今天还没正式开始上课哦，尽情享受假期吧！\n")
        else:
          i = i+1
          continue
      if string_class_today == str(" "):
        return words_no_class_today
      else:
        return string_class_today
  else:
    notice_txt = ("\n当前课程表功能未启用，请检查配置文件或删除模板变量timetable\n")
    print(notice_txt)
    return notice_txt




