import sys, os
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
logger = logging.getLogger("config.py")
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
#class MpulseConfig()

def getCredentials(config_file, section_name):
    settings = {}
    #logger.getLogger("config.py:getCredentials")    
    expanded_config_file = os.path.expanduser(config_file)
    if os.path.isfile(expanded_config_file):
        logger.debug(expanded_config_file + ' file found and valid.')
        mpulse_config = ConfigParser()
        mpulse_config.readfp(open(expanded_config_file))
        if mpulse_config.has_section(section_name):
            for key,value in mpulse_config.items(section_name):
                settings[key] = value
            logger.debug(settings)
        else:
            logger.error('Unable to find section: ' + section_name)
    else:
        logger.error('Invalid or wrong config file: ' + expanded_config_file)
    return settings
    

def generateToken(apitoken, tenant):
    security_token = {}

    #first check if the credential file already exists.
    stored_security_token_file = os.path.expanduser("~/.mpulse_security_token")
    if os.path.isfile(stored_security_token_file):
        #security token file already exists - check if it is older than 5 hrs
        try:
            stat_result = os.stat(stored_security_token_file)
            # if the file is less than 5 mins old
            if mpulse_helper.check_age(stat_result.st_ctime) < 300:            
                with open(stored_security_token_file) as f:
                    security_token = json.loads(f.read())   
                    logger.info("Read security credentials from file.")     
        except Exception as e:
            logger.error("Unable to open stored credentials at " + stored_security_token_file + "\n" + str(e))

    if security_token == {}:  
        logger.info("No stored credentials was used - invoking the call now..")  
        token_url = "https://mpulse.soasta.com/concerto/services/rest/RepositoryService/v1/Tokens"
        payload = {"apiToken": apitoken}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if tenant != None and tenant!="":
            payload["tenant"] = tenant
        
        logger.debug('Using the body: ' + str(payload))        
        response = requests.put(token_url, data=json.dumps(payload), headers=headers)
        if response.status_code != 200:
            logger.error("Error in creating a token")
            logger.error(response.headers)
        else:
            security_token = json.loads(response.text)
            logger.info("received the token: " + json.dumps(security_token))

    # finally, re-write the credentials so that we will get the next updated time
    try:
        with open(stored_security_token_file, "w") as f:
            f.write(json.dumps(security_token))
    except Exception as e:
        logger.error("Unable to write the credentials: " + str(e))
    
    return security_token

def getToken(config_file, section):
    '''
        Takes the apitoken and tenant as input parameter and responds back with a security token that is created.
    '''
    token = {}

    settings = getCredentials(config_file, section)

    if settings != {}:        
        if ('apitoken' in settings) and ('tenant' in settings):
            token = generateToken(settings['apitoken'], settings['tenant']) 
        else:
            logger.error("Unable to find apiToken")  
    else:
        logger.error("Unable to generate a token.") 
    
    return token

if __name__=="__main__":    

    parser = argparse.ArgumentParser(description='mPulse entry point.' )
    parser.add_argument('--config', help='mPulse configuration file containing the user\'s API key (deault=~/.mpulse)',default="~/.mpulse")
    parser.add_argument('--section', help='Section within the config file containing the credentials (default=[mpulse])',default='mpulse')    
    args = parser.parse_args()
    logger.debug('Configuration file: ' + args.config)
    logger.debug('Configuration section: ' + args.section)
    settings = getCredentials(args.config,args.section)
    generateToken(settings['apitoken'], settings['tenant'])