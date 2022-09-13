from distutils.command.config import config
import sys
import time
import argparse
import subprocess
import schedule
import signal

from timetable import get_timetable_config


parser = argparse.ArgumentParser()
parser.add_argument('--cfg', type=str, default='config.yaml')
args = parser.parse_args()


def send_message_now():
    print("running...")
    subprocess.run([f"{sys.executable}", "main.py"])
    return


def signal_handler(signum, frame):
    print("\n程序结束！")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)



        
if __name__ == '__main__':


    print("开始运行，等待定时触发...")

    daily_time = get_timetable_config("DAILY_TIME")
    schedule.every().day.at(daily_time).do(send_message_now)

    while True:
        schedule.run_pending()
        time.sleep(50) # wait
