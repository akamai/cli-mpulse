'''
Helper function for running the mPulse REST API
'''

def build_query_string(query_arguments):
	'''		
		Takes the input as a dictionary and returns a list of 'name=value' result. 
		This will be used later to build the final set of query string.
	'''
	query_string_list = []
	for each_key in query_arguments:
		query_string_list.append(each_key+'='+query_arguments[each_key])
	return query_string_list

def get_query_date(arguments):
	'''
		This function tries to find if the input has 'date' parameter
		or if a 'date-comparator' was provided.
		If both date and date-comparator is provider, it will default to 
		date-comparator=LastHour
	'''
	query_arguments = {}
	if 'date-comparator' not in arguments and 'date' not in arguments:
		#nothing specific is given. simply use LastHour
		query_arguments["date-comparator"] = "LastHour"
	else:
		#only date is provided
		if 'date' in arguments:
			query_arguments["date"] = arguments["date"]
		else:
			if 'date-compartor' in arguments['date-comparator']:
				query_arguments['date-comparator'] = arguments['date-comparator']
	return query_arguments

def cleanup_arguments(arguments):
	'''
		This function simply removes a bunch of dictionary elements. This step is necessary
		as we take the incoming arguments and build the final query string
	'''
	arguments.pop('type', None)
	arguments.pop('date-comparator', None)
	arguments.pop('date', None)
	arguments.pop('startdate', None)
	arguments.pop('enddate', None)
	return arguments