'''
Provides a CLI-like functionality for the mPulse Query API
'''
import sys
import config
if sys.version_info[0] >= 3:
     # python3
     from configparser import ConfigParser
     import http.client as http_client
else:
     # python2.7
     from ConfigParser import ConfigParser
     import httplib as http_client

import argparse
import logging
import requests
import json
import mpulse_helper

#setup logging
logger = logging.getLogger("mpulse_wrapper.py")
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


def getApiResponse(token, args):
	'''
		Single wrapper for all the calls for mPulse Query API.
		It takes the security token and the incoming arguments and the output is a JSON response.
	'''
	base_url = "https://mpulse.soasta.com/concerto/mpulse/api/v2/"

	# extract arguments from the command line, including the command type
	arguments = {}
	if 'args' in args and args.args != None or args.args!="":		
		for each_argument in args.args:
			params = each_argument.strip().split("=")
			if len(params) == 2:
				arguments[params[0]] = params[1]
	if 'type' not in arguments:
		arguments['type'] = "summary"

	function = '/' + arguments['type']
	
	query_arguments = mpulse_helper.get_query_date(arguments)
	query_arguments['format'] = 'json'
	
	# cleanup the list of "arguments" to remove the ones we already used
	mpulse_helper.cleanup_arguments(arguments)	
	#merge the arguments dictionary to query_arguments dictionary. we'll use 'query_arguments' to build the final set of query strings
	query_arguments.update(arguments)	
	logger.debug("Arguments currently in list: " + str(query_arguments))

	# add the necessary auth token header
	headers = {"Authentication": token["token"]}

	#build the final api endpoint
	api_endpoint = base_url + args.api_key + function + "?" + "&".join(mpulse_helper.build_query_string(query_arguments))
	
	logging.debug("API URL: " + api_endpoint)
	response = {}

	#make the call and send back the response
	try:
		response = requests.get(api_endpoint, headers = headers)
		if response.status_code == 200:
			logger.info(json.dumps(response.json(),indent=2))	
			response = response.json()		
	except Exception as e:
		logging.error(str(e))
	
	return response		

if __name__=="__main__":    

    parser = argparse.ArgumentParser(description='CLI for mPulse Query API. For more information about the API, please refer to https://developer.akamai.com/api/web_performance/mpulse_query/v2.html' )
    parser.add_argument('--config', help='mPulse configuration file containing the user\'s API key (deault=~/.mpulse)',default="~/.mpulse")
    parser.add_argument('--section', help='Section within the config file containing the credentials (default=[mpulse])',default='mpulse')
    parser.add_argument('--api_key', help='API key of the app',required=True) 
    parser.add_argument('--timer', help='The timer to report (default=page load time)', default='PageLoad')
    #gather up reminder
    parser.add_argument('args', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    logger.debug('Configuration file: ' + args.config)
    logger.debug('Configuration section: ' + args.section)
    logger.debug(args)

    ## first create a security token
    token = config.getToken(args.config,args.section)    
    logger.debug(token)

    ## now fire the API call
    getApiResponse(token, args)    
