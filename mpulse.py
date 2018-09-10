import requests
import subprocess
import json
#
import http.client as http_client
http_client.HTTPConnection.debuglevel = 1

def generate_token():
    #headers = {"Content-Type": "application/json"}
    resp = subprocess.check_output(["curl", "-s","--request", "PUT", "https://mpulse.soasta.com/concerto/services/rest/RepositoryService/v1/Tokens", "--data-binary", '{"apiToken": "1c582737-252b-43ba-bb9a-e17747df48f0","tenant": "Macys mPulse"}'])
    data = json.loads(resp)
    token = data['token']
    return token

def get_summary(token):
    '''
    api_key= "WVZ92-598Q4-C592Z-HWSHG-PBBKW"
    headers = {"User-Agent": "curl", "Authentication": token}
    resp = requests.get("https://mpulse.soasta.com/concerto/mpulse/api/"+api_key+"/summary?date=2018-05-20",headers=headers)
    print (resp.status_code, resp.headers)
    '''
    resp = subprocess.check_output(["curl", "-H","Authentication:a123b53a-440-133-4638-ad5b-4c54fabbd788", "https://mpulse.soasta.com/concerto/mpulse/api/v2/WVZ92-598Q4-C592Z-HWSHG-PBBKW/summary?date=2018-05-20","-s"])
    data = json.loads(resp)
    print (json.dumps(data, indent=2))



if __name__=="__main__":
    token = "7ca74dcd-be0-135-4fe1-8af8-6174ec4a35fd"
    token = generate_token()
    get_summary(token)