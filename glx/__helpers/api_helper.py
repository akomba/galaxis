import requests
import json
from glx.logger import Logger

TIMEOUT = 20
DEBUG = False


def call_api(url,reqtype,**kwargs):
    lg = Logger()
    api_key = kwargs.get("api_key",None)
    data = kwargs.get("data",None)
    if DEBUG:
        print(">>>API URL: >"+reqtype[:3]+"< "+url)
    
    if api_key:
        if reqtype == "get":
            headers = {'x-api-key': api_key, "accept":"application/json"}
        else:
            headers = {'x-api-key': api_key, "Content-Type":"application/json"}
    else:
        headers = {}
       
    try:
        if reqtype == "get":
            response = requests.get(url, headers=headers, timeout=TIMEOUT)
        elif reqtype == "delete":
            if data:
                response = requests.delete(url, headers=headers, data=json.dumps(data),timeout=TIMEOUT)
            else:
                response = requests.delete(url, headers=headers,timeout=TIMEOUT)
        elif reqtype == "put":
            if data:
                response = requests.put(url, headers=headers, data=json.dumps(data),timeout=TIMEOUT)
            else:
                response = requests.put(url, headers=headers,timeout=TIMEOUT)
        elif reqtype == "patch":
            if data:
                response = requests.patch(url, headers=headers, data=json.dumps(data),timeout=TIMEOUT)
            else:
                response = requests.patch(url, headers=headers,timeout=TIMEOUT)
        elif reqtype == "post":
            if data:
                response = requests.post(url, headers=headers, data=json.dumps(data),timeout=TIMEOUT)
            else:
                response = requests.post(url, headers=headers,timeout=TIMEOUT)
        else:
            print("API BAD REQ: " +reqtype+" "+url)
            lg.logger.debug("API BAD REQ: " +reqtype+" "+url)
            return None

    except requests.exceptions.RequestException as e:
        print('Error:', e)
        lg.logger.debug("API ERROR: " +str(e) +" "+reqtype+" "+url)
        return None

    if response.status_code in [200,201,204]:
        lg.logger.info("API: "+str(response.status_code)+" "+reqtype+" "+url)
        #if DEBUG:
        #    print(">>>API "+str(response.status_code)+"    "+reqtype[:3]+" "+url)
        if response.status_code == 204:
            return None
        else:
            assets = response.json()
            return assets
    else:
        print('Error:', response.status_code)
        #print(curl_request(url,"GET",headers,None))
        lg.logger.debug("API BAD RESP: " +str(response.status_code) +" "+reqtype+" "+url)
        return None


def curl_request(url,method,headers,payloads):
    # construct the curl command from request
    command = "curl -v -H {headers} {data} -X {method} {uri}"
    data = "" 
    if payloads:
        payload_list = ['"{0}":"{1}"'.format(k,v) for k,v in payloads.items()]
        data = " -d '{" + ", ".join(payload_list) + "}'"
    header_list = ['"{0}: {1}"'.format(k, v) for k, v in headers.items()]
    header = " -H ".join(header_list)
    print(command.format(method=method, headers=header, data=data, uri=url))
