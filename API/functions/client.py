import requests,json,imp,ConfigParser

def get_server_ip(): #Retrieve alert collector ip from configuration file
	server = '/opt/isms/API/config/server/server_conf.ini'
	config = ConfigParser.RawConfigParser()
	config.read(server)
	url = config.get('server','ip')
	return url

def register_alert_generator(name,author,ip,key): # Register alert generator
	url = get_server_ip()
   	URL = 'http://'+url+':8000/generators/add/'
	string='{"name":"'+name+'","author":"'+author+'","ip":"'+ip+'","key":"'+str(key)+'"}'
	payload ={'data':string} # type<'dict'>
	response = requests.post(URL,data=payload)
	print response.content

register_alert_generator("HIDS","admin",'127.0.0.1',123) 

def verify_alert_generator(name,author,ip,key): # Verify alert generator
	url = get_server_ip()
	URL = 'http://'+url+':8000/generators/verify/'
  	string='{"name":"'+name+'","author":"'+author+'","ip":"'+ip+'","key":"'+str(key)+'"}'
       	payload ={'data':string} # type<'dict'>
        response = requests.post(URL,data=payload)
	print response.content

verify_alert_generator("HIDS","admin",'127.0.0.1',123)

def update_alert_generator(name,author,ip,key,args): #Update alert generator
	url = get_server_ip()
        URL = 'http://'+url+':8000/generators/update/'
       	string='{"name":"'+name+'","author":"'+author+'","ip":"'+ip+'","key":"'+str(key)+'","args":"'+str(args)+'"}'
        payload ={'data':string} # type<'dict'>
        response = requests.post(URL,data=payload)
        print response.content

update_alert_generator("NIDS","admin",'127.0.0.1',123,{"name":"NIDS"})

def delete_alert_generator(name,author,ip,key): #Delete alert generator
	url = get_server_ip()
        URL = 'http://'+url+':8000/generators/del/'
        string='{"name":"'+name+'","author":"'+author+'","ip":"'+ip+'","key":"'+str(key)+'"}'
        payload ={'data':string} # type<'dict'>
        response = requests.post(URL,data=payload)
        print response.content

delete_alert_generator("HIDS","admin","127.0.0.1",123)

def register_alert_group(name,desc,generator,author,key,ip): #Register alert group
    url = get_server_ip()
    URL = 'http://'+url+':8000/groups/add/'
    string = '{"name":"'+name+'","description":"'+desc+'","author":"'+author+'","generator":"'+generator+'","key":"'+str(key)+'","ip":"'+ip+'"}'
    payload = {'data':string} # type<'dict'>
    response = requests.post(URL,payload)
    print response.content

register_alert_group("hids_FTP","protocol","HIDS","admin",123,"127.0.0.1");

def delete_alert_group(name,desc,generator,author,key,ip): #Delete alert group
	url = get_server_ip()
	URL = 'http://'+url+':8000/groups/del/'
	string = '{"name":"'+name+'","description":"'+desc+'","author":"'+author+'","generator":"'+generator+'","key":"'+str(key)+'","ip":"'+ip+'"}'
	payload = {'data':string} # type<'dict'>
	response = requests.post(URL,payload)
	print response.content

register_alert_group("hids_FTP","protocol","HIDS","admin",123,"127.0.0.1")

def verify_alert_group(name,desc,generator,author,key,ip): #Verify alert group
        url = get_server_ip()
        URL = 'http://'+url+':8000/groups/verify/'
        string = '{"name":"'+name+'","description":"'+desc+'","author":"'+author+'","generator":"'+generator+'","key":"'+str(key)+'","ip":"'+ip+'"}'
        payload = {'data':string} # type<'dict'>
        response = requests.post(URL,payload)
        print response.content
verify_alert_group("hids_FTP","protocol","HIDS","admin",123,"127.0.0.1")

def update_alert_group(name,desc,generator,author,key,ip,args): #Update alert group
	url = get_server_ip()
	URL = 'http://'+url+':8000/groups/update/'
	string = '{"name":"'+name+'","description":"'+desc+'","author":"'+author+'","generator":"'+generator+'","key":"'+str(key)+'","ip":"'+ip+'","args":"'+str(args)+'"}'
	payload = {'data':string} # type<'dict'>
	response = requests.post(URL,data=payload)
	print response.content

update_alert_group("FTP","protocol","HIDS","admin",123,"127.0.0.1",{"description":"protocol"})

def register_alert_class(name,desc,help,syntax,filter,parent,group,key,ip): #Register alert class
	url =get_server_ip()
	URL = 'http://'+url+':8000/class/add/'
	string = '{"name":"'+name+'","description":"'+desc+'","help":"'+help+'","syntax":"'+syntax+'","filter":"'+filter+'","parent":"'+parent+'","group":"'+group+'","key":"'+str(key)+'","ip":"'+ip+'"}'
	payload = {'data':string} # type<'dict'>
	response = requests.post(URL,payload)
	print response.content
register_alert_class("TCPPORT_MISSING","ACD","ACH","TCPPORT:port","","TCPPORT_MISSING","hids_FTP",123,"127.0.0.1")
