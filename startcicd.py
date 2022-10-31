#!/usr/bin/env python3

import json
import requests
import sys
import time


settingsfile    = 'settings.json'


## Functions

def return_url ( settingsobject ):
    
    """
    input:
    - settingsobject : JSOn object

    returns constructed url & httheaders if required

    This function reads cli arguments and reads corresponding settings from json file.
    It constructs the url for the API call & the required http headers.
    """
    a = sys.argv
    url = ""
    httpheaders = {}

    if 'startgns3' in a[1:] or 'stopgns3' in a[1:]: #It is a call to a GNS3 project
        toplevelkey = 'gns3'
        s = settingsobject[toplevelkey]
        url = s['prot']+s['serverip']+":"+s['serverport']+"/"+s['projecturi']+"/"+s['project']
        if 'startgns3' in a[1:]: url = url+"/"+s['nodesstarturi']
        if 'stopgns3' in a[1:]: url = url+"/"+s['nodesstopuri']
    elif 'launchawx' in a[1:]: #It is a call to Ansible Tower
        toplevelkey = 'awx'
        s = settingsobject[toplevelkey]
        url = s['prot']+s['serverip']+":"+s['serverport']+"/"+s['projecturi']+"/"+s['jobtemplateid']+"/"+s['launchsuffix']+"/"
    
    else: #No cli arguments given
        print('\nusage : ' + sys.argv[0] + ' <option>\n')
        print(' - startgns3 : will start GNS3 project')
        print(' - stopgns3  : will stop GNS3 project')
        print(' - launchawx : will start job template on Ansible tower')
        print('=========================================================')
        sys.exit()

    if 'httpheaders' in s: httpheaders = s['httpheaders']

    return url, httpheaders, { "runtype" : toplevelkey }


def readsettings ( jsonfile ):

    """
    input
    - jsonfile : json file with all settings

    return
    - json object with all settings
    """

    try:
        f       = open(jsonfile)
        data    = json.load(f)

    except:
        result  = { "tryerror" : "Error reading settings file " + jsonfile }

    else:
        result = data
    
    f.close()
    return result


def request ( url, reqtype, jsondata={} ):
    
    """
    input
    - url : array object with url and headers
    
    return
    - http request result

    This function requests an api call to the url endpoint.
    """
    
    if reqtype == 'post':
        #print(url)
        #print(url[0])
        #print(url[1])
        r = requests.post ( url[0], headers=url[1], data=jsondata )
    elif reqtype == 'get': r = requests.get ( url[0], headers=url[1] )
    obj = r.content.decode('utf-8') #from bytes to dict
    #print(obj)
    
    return obj


def jobstatuschecker ( dataobject ):
    
    status   = ''
    failed   = ''
    finished = ''
    proceed  = False #This can be used by Jenkins to determine if Chain is continuoud
    st       = 10 #Delay between check requests
    
    if type(dataobject) == str: dataobject = json.loads(dataobject) #From str to json
 
    urisuffix = dataobject['url'] #Catch the job url that was created
    s = settings['awx']
    url = s['prot']+s['serverip']+":"+s['serverport']+urisuffix #create uri for API call to awx to check job status
    myurltuple = ( url, urltuple[1] ) #Create urltuple with url and headers
   
    # start Loop, get every 10 seconds jobstatus
    #
    # - jobstatus   (can be pending, running, failed)
    # - jobfailed   (can be false, true)
    # - jobfinished (can be null or time, i.e 2022-10-24T14:38:50.009531Z)

    print('\n Starting jobchecker. Waiting till AWX template finishes its job...')

    while True:
    
        response = request ( myurltuple, "get" ) #Request API call
        if type(response) == str: response = json.loads(response) #From str to json
    
        result = { 
                   "jobstatus"   : response['status'],
                   "jobfailed"   : response['failed'],
                   "jobfinished" : response['finished']
                 }

        status   = result['jobstatus'].lower()
        failed   = result['jobfailed']
        finished = result['jobfinished']
    
        if status == 'succesful':
            if failed == 'false' or failed == False:
                print('\n Succesful job finish at ' + finished)
                proceed = True
                break
            else:
                print('\n Job finished succesful but with failed result.')
                break
            cont
        elif status == 'failed':
            if finished != None and finished != 'null':
                print('\n Job finished with "failed" status. Check job logs on AWX. Will not proceed.')
                break
            else:
                print('\n Job finished with "failed" status due to finish errors. Will not proceed.')

        print('  Job status : ' + status + '. Wait ' + str(st) + ' secs till next check..')
        time.sleep(st)

    print()

    return proceed #returns the status of the job that was started

    


########################
##### MAIN PROGRAM #####
########################

settings = readsettings ( settingsfile ) #Read settings to JSON object

# Request API call
urltuple = return_url ( settings ) #Return required URL, headers if needed & other option data
response = request ( urltuple, "post") #Request API POST request
#print(response)
#If AWX project was launched, check its jobstatus till finished
if 'awx' in urltuple[2]['runtype']:
    checkresult = jobstatuschecker ( response )
    #print(checkresult)


