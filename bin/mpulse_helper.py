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

def get_query_date(arguments):
	'''
		This function tries to find if the input has 'date' parameter
		or if a 'date-comparator' was provided.
		If both date and date-comparator is provider, it will default to 
		date-comparator=LastHour
	'''
	query_arguments = {}
	if 'date-comparator' not in arguments and ('date' not in arguments or ('date-start' not in arguments and 'date-end' not in arguments) ):
		#nothing specific is given. simply use LastHour
		query_arguments["date-comparator"] = "LastHour"
	else:
		#only date is provided
		if 'date' in arguments:
			query_arguments["date"] = arguments["date"]
		else:
			if 'date-comparator' in arguments:
				query_arguments['date-comparator'] = arguments['date-comparator']

			#check if date-start and date-end have been provided as well
			if 'date-start' in arguments and 'date-end' in arguments:
				query_arguments['date-start'] = arguments['date-start']
				query_arguments['date-end'] =arguments['date-end']
				query_arguments['date-comparator'] = 'Between'
	return query_arguments

def cleanup_arguments(arguments):
	'''
		This function simply removes a bunch of dictionary elements. This step is necessary
		as we take the incoming arguments and build the final query string
	'''
	arguments.pop('type', None)
	arguments.pop('date-comparator', None)
	arguments.pop('date', None)
	arguments.pop('date-start', None)
	arguments.pop('date-end', None)
	return arguments

def check_age(file_timestamp):
	#get the current timestamp
	current_timestamp = calendar.timegm(time.gmtime())
	return (current_timestamp - file_timestamp)

def print_response(response):
	'''
		This function tried to print a human friendly format of the API response.
		For typical calls like summary, etc, the response will contain the median, 95th percentile and so on.
		For some special calls when such data is not available, the response is to dumpt th eJSON
	'''
	if 'median' in response and 'p98' in response and 'p95' in response and 'moe' in response and 'n' in response:
		response['median'] = float(response['median']) / 1000
		response['p95'] = float(response['p95']) / 1000
		response['p98'] = float(response['p98']) / 1000
		response['moe'] = float(response['moe']) / 1000


		print("------------------------------------------------------")
		print("Total beacons: " + str(response['n']))		
		print("Median: " + str( response['median'] ) + " s" )
		print("95th Percentile: " + str( response['p95'] ) + " s")
		print("98th Percentile: " + str( response['p98'] ) + " s")
		print("Margin of Error: " + str( response['moe'] ) + " s")
		print("------------------------------------------------------")
	else:
		print(json.dumps(response, indent=2))