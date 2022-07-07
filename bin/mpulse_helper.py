from __future__ import print_function
import time
import calendar
import urllib
import json

'''
Helper function for running the mPulse REST API
'''

def check_age(file_timestamp):
    #get the current timestamp
    current_timestamp = calendar.timegm(time.gmtime())
    return (current_timestamp - file_timestamp)

def print_response(opt, response):
    '''Prints response to stdout. Prints in JSON if opt.json is true.'''
    if opt.json:
        print(json.dumps(response))
    else:
        print("======================================================")
        print(f"Report Type: {opt.type}")
        print(f"Reporting timer: {opt.timer}")
        print(f"Reporting metric: {opt.metric}")
        if opt.date:
            print(f"Date: {opt.date}")
        else:
            print(f"Period ({opt.date_comparator}): {opt.date_start} / {opt.date_end}")

        print("------------------------------------------------------")
        print(f"Total count: {response.get('n')}")
        print(f"Median: {response.get('median')}")
        print(f"95th Percentile: {response.get('p95')}")
        print(f"98th Percentile: {response.get('p98')}")
        print(f"Margin of Error: {response.get('moe')}")
        print("------------------------------------------------------")
        for k in sorted(response.keys()):
            print(f"{k}: {response[k]}")
        print("------------------------------------------------------")
