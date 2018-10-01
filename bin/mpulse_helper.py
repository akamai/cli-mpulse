from __future__ import print_function
import time
import calendar
import urllib
import json


'''
Helper function for running the mPulse REST API
'''

def build_query_string(query_arguments):
	'''		
		Takes the input as a dictionary and returns a list of 'name=value' result. 
		This will be used later to build the final set of query string.
	'''
	
	return urllib.urlencode(query_arguments)

def get_query_date(date_comparator, date, date_start, date_end):
	'''
		This function tries to find if the input has 'date' parameter
		or if a 'date-comparator' was provided.
		If both date and date-comparator is provider, it will default to 
		date-comparator=LastHour
	'''
	query_arguments = {}
	
	query_arguments["date-comparator"] = date_comparator
	
	#only date is provided
	if date!= None:
		query_arguments["date"] = date
	

	#check if date-start and date-end have been provided as well
	if date_start != None and date_end!= None:
		query_arguments['date-start'] = date_start
		query_arguments['date-end'] = date_end
		query_arguments['date-comparator'] = 'Between'

	return query_arguments

def cleanup_arguments(arguments):
	'''
		This function simply removes a bunch of dictionary elements. This step is necessary
		as we take the incoming arguments and build the final query string
	'''
	#arguments.pop('type', None)
	if 'date' in arguments:
		arguments.pop('date-comparator', None)
		arguments.pop('date-start', None)
		arguments.pop('date-end', None)	
	return arguments

def check_age(file_timestamp):
	#get the current timestamp
	current_timestamp = calendar.timegm(time.gmtime())
	return (current_timestamp - file_timestamp)

def print_response(report_type, timer, date_comparator, date, date_start, date_end, response):
	'''
		This function tried to print a human friendly format of the API response.
		For typical calls like summary, etc, the response will contain the median, 95th percentile and so on.
		For some special calls when such data is not available, the response is to dumpt th eJSON
	'''
	if 'median' in response and 'p98' in response and 'p95' in response and 'moe' in response and 'n' in response:
		
		response['n'] = int(response['n']) if (response['n'] != None) else 0
		response['median'] = float(response['median']) / 1000 if (response['median'] != None) else 0.0
		response['p95'] = float(response['p95']) / 1000 if (response['p95'] != None)  else 0.0
		response['p98'] = float(response['p98']) / 1000 if (response['p98'] != None) else 0.0 
		response['moe'] = float(response['moe']) / 1000 if (response['moe'] != None) else 0.0 

		print("======================================================")
		print("Report Type: " + report_type)
		print("Reporting metric: " + timer)
		print("Reporting period: ", end="")
		if date!= None:
			print(date)
		else:
			if date_start != None and date_end != None:
				print("Between " + date_start + " - " + date_end)
			else:
				print(date_comparator)
		print("------------------------------------------------------")
		print("Total beacons: " + str(response['n']) )		
		print("Median: " + str( response['median'] ) + " s" )
		print("95th Percentile: " + str( response['p95'] ) + " s")
		print("98th Percentile: " + str( response['p98'] ) + " s")
		print("Margin of Error: " + str( response['moe'] ) + " s")
		print("------------------------------------------------------")
	else:
		print(json.dumps(response, indent=2))