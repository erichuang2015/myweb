import os.path
import time
import json


def log(*args, **kwargs):
    # time.time() 返回 unix time
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('boyka.log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, **kwargs)
        print(dt, *args, file=f, **kwargs)

def formatted_time(unixtime):
    time_format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(unixtime))
    formatted = time.strftime(time_format, value)
    return formatted