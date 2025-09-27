import requests
import json

TIMEOUT = 10

def call_api(url,api_key=None):
    url = url+"?limit=20000&page=1"
    assets = _call_api(url,api_key)
    if assets is None:
        return None

    #if "pagination" in assets:
    #    # determine number of pages
    #    assets = _call_api(url+"?limit=100")
    #    pag = assets["pagination"]
    #    #print(pag)
    #    for p in range(2,pag["pages"]+1):
    #        #print("getting page",p)
    #        a = _call_api(url+"?limit=100&page="+str(p))
    #        assets["data"]+=a["data"]

    return assets

def delete(url,api_key,data):
    headers = {'x-api-key': api_key, "Content-Type":"application/json"}
    try:
        response = requests.delete(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            return response.status_code
        else:
            print('Error:', response.status_code)
            return None

    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def put(url,api_key,data):
    headers = {'x-api-key': api_key, "Content-Type":"application/json"}
    try:
        response = requests.put(url, headers=headers, data=json.dumps(data),timeout=TIMEOUT)

        if response.status_code in [200,201]:
            return response.status_code
        else:
            print('Error:', response.status_code)
            return None

    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def _call_api(url,api_key=None):
    try:
        if api_key:
            headers = {'x-api-key': api_key, "accept":"application/json"}
            #response = requests.get(url,headers,timeout=TIMEOUT)
        else:
            headers = {}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            assets = response.json()
            return assets
        else:
            print('Error:', response.status_code)
            print(curl_request(url,"GET",headers,None))
            return None

    except requests.exceptions.RequestException as e:
        print('Error:', e)
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
