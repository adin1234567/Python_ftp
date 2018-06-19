import os
import schedule
import time

def job():
    os.system('python Iot_ftp.py')

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)