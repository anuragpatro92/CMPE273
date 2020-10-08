import schedule
import time
import yaml
import json
import sys
from Step import Step
import requests



step = None
time = None
allsteps = dict()
to_execute = list()

#get id from the json object of eac step
def get_id(map):
    for key in map:
        return key


#read the yml file and store the data in a dictionary of steps
def read_yml(filePath):
    with open(filePath) as f:
        global time
        global to_execute
        # use safe_load instead load
        dataMap = yaml.safe_load(f)
        #print(dataMap)

        for i in range(len(dataMap['Steps'])):
            id = get_id(dataMap['Steps'][i])
            map = dataMap['Steps'][i][id]
            #print(map)
            step = Step(id,map['outbound_url'],map['condition'],map['method'])
            allsteps[id] = step

        time= dataMap['Scheduler']['when']
        to_execute = dataMap['Scheduler']['step_id_to_execute']


#schedule week day runs
def schudle_week(time_to_run,day):
    if day == '0':
        schedule.every().monday.at(time_to_run).do(lambda: job())
    elif day == '1':
        schedule.every().tuesday.at(time_to_run).do(lambda: job())
    elif day == '2':
        schedule.every().wednesday.at(time_to_run).do(lambda: job())
    elif day == '3':
        schedule.every().thursday.at(time_to_run).do(lambda: job())
    elif day == '4':
        schedule.every().friday.at(time_to_run).do(lambda: job())
    elif day == '5':
        schedule.every().saturday.at(time_to_run).do(lambda: job())
    elif day == '6':
        schedule.every().sunday.at(time_to_run).do(lambda: job())
    else :
        print('invalid')

#genric schdule method
def schduledemo():
    #print(time)
    temp = time.split(' ')

    minutes = temp[0]
    hrs = temp[1]
    day = temp[2]
    #print(hrs)

    if((minutes != '*') & (hrs == '*') & (day == '*') ):

        schedule.every(int(minutes)).minutes.do(lambda: job())
    elif((minutes == '*') & (hrs != '*') & (day == '*') ):
        if (int(hrs) < 10):
            hrs = '0' + hrs
        time_to_run = str(hrs) + ':' + '00'
        schedule.every().day.at(time_to_run).do(lambda: job())
    elif((minutes == '*') & (hrs == '*') & (day != '*')):
        time_to_run = '00' + ':' + '00'
        schudle_week(time_to_run,day)
    elif((minutes != '*') & (hrs != '*') & (day == '*') ):
        if(int(minutes) < 10):
            minutes = '0' + minutes
        if (int(hrs) < 10):
            hrs = '0' + hrs
        time_to_run = hrs+':'+minutes
        schedule.every().day.at(time_to_run).do(lambda: job())
    elif((minutes != '*') & (hrs == '*') & (day != '*')):
        if (int(minutes) < 10):
            minutes = '0' + minutes
        time_to_run =  '00' + ':' + minutes
        schudle_week(time_to_run, day)
    elif((minutes == '*') & (hrs != '*') & (day != '*')):
        if(int(hrs) < 10):
            hrs = '0' + hrs
        time_to_run = hrs + ':' + '00'
        schudle_week(time_to_run, day)
    elif((minutes != '*') & (hrs != '*')& (day != '*')):
        if (int(minutes) < 10):
            minutes = '0' + minutes
        if (int(hrs) < 10):
            hrs = '0' + hrs
        time_to_run = hrs + ':' + minutes
        schudle_week(time_to_run, day)
    else :
        print('wrong time')


#start execution
def start(filePaths):
    #print(filePaths)
    if len(filePaths) != 0:
        read_yml(filePaths[1])
        schduledemo()

        while True:
            schedule.run_pending()
    else:
        print('no file name passed')



#execution method of step
def apiCall(step, url):

    if(step.outbound_url != '::input:data'):
        url = step.outbound_url

    condition = step.condition
    try:
        responses = requests.request(step.method,url)
        left = condition['if']['equal']['left']
        right = condition['if']['equal']['right']
        if ((left == 'http.response.code') & (str(right) == str(responses.status_code))):
            action = condition['then']['action']
            data = condition['then']['data']
            if 'invoke' in action:
                to_step = action.split(':')
                id = int(to_step[-1])
                apiCall(allsteps[id], data)
            elif 'print' in action:
                display(data, responses)
        else:
            print('error...')
    except:
        action = condition['else']['action']
        data = condition['else']['data']
        if 'invoke' in action:
            to_step = action.split(':')
            id = int(to_step[-1])
            apiCall(allsteps[id], data)
        elif 'print' in action:
            display(data,None)



#display required
def display(data,responses):

    if data == 'http.response.headers.X-Ratelimit-Limit':
        print(responses.headers.get('X-Ratelimit-Limit'))
    elif data == 'http.response.code':
        print(responses.status_code)
    elif data == 'http.response.headers.content-type':
        print(responses.headers.get('content-type'))
    else :
        print(data)







# job controller
def job():
    #responses = http_client(config)
    for i in range(len(to_execute)):
        #print(to_execute[i])
        apiCall(allsteps[to_execute[i]],None)



if __name__ == '__main__':
    start(sys.argv)




#http_client