import schedule
import time
import yaml
import json
from Step import Step
import requests


step = None
time = None

def read_yml(filePath):
    with open(filePath) as f:
        # use safe_load instead load
        dataMap = yaml.safe_load(f)
        print(dataMap['Step'])
        print(dataMap['Scheduler']['when'])
        time = dataMap['Scheduler']['when']
        step = Step(dataMap['Step']['id'],dataMap['Step']['outbound_url'],dataMap['Step']['condition'])
    return step

def schduledemo(step):

    schedule.every(0.1).minutes.do(lambda: job(step))
    schedule.every().hour.do(lambda: job(step))
    schedule.every().day.at("10:30").do(lambda: job(step))
    schedule.every(5).to(10).minutes.do(lambda: job(step))
    schedule.every().monday.do(lambda: job(step))
    schedule.every().wednesday.at("13:15").do(lambda: job(step))
    schedule.every().minute.at(":17").do(lambda: job(step))

def start():
    step = read_yml('Test.yaml')
    schduledemo(step)

    while True:
        schedule.run_pending()

def job(step):
    responses = requests.get(step.outbound_url)
    print(responses)

start()

