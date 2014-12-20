import requests,json,psycopg2,logging,ConfigParser

def get_ip(name):
	LOG_FILENAME = '/opt/isms/isms/log/client.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,datefmt='%a, %d %b %Y %H:%M:%S',format='%(asctime)s %(levelname)-8s %(message)s\n')
	try:
		logging.debug('Connecting to database') #Getting IP of alert generator
		server = '/opt/isms/isms/config/server/server_conf.ini'
	        config = ConfigParser.RawConfigParser()
        	config.read(server)
	        user = config.get('database','user')
		pswd = config.get('database','password')
		dbname = config.get('database','name')
		conn = psycopg2.connect(database=dbname,user=user,password=pswd)
	except psycopg2.OperationalError as e:
		logging.exception('Database not running')
		return None
	else:
		cur = conn.cursor()
		logging.debug('Retieving ip address')
		cur.execute("SELECT alert_gen_ip from alertgenerator where alert_gen_name=(%s)",(name,))
		result = cur.fetchone()
		if result:		
			logging.info('IP address retrieved')
			ip = result[0]
		else:
			logging.info('No matching generator found in the database')
			ip = result
		conn.commit()
		cur.close()
		conn.close()
		logging.debug('Connection to database closed')
		return ip

get_ip("HIDS")

def instantiate_alert_generator(gen_name,alert_class,alert_id,args):
	ip = get_ip(gen_name)	
	LOG_FILENAME = '/opt/isms/isms/log/client.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,datefmt='%a, %d %b %Y %H:%M:%S',format='%(asctime)s %(levelname)-8s %(message)s\n')
	if ip: 
		logging.debug('IP address retrieved '+ip)
		URL = 'http://'+ip+':8080/instance/' # URL of alert generator
		string = '{"generator":"'+gen_name+'","class":"'+alert_class+'","id":"'+str(alert_id)+'","args":"'+str(args)+'"}'
		payload = {"data":string} # type<'dict'>
		logging.info('Sending POST Request to instantiate alert generator '+gen_name)
		response = requests.post(URL,data=payload)	
		logging.info('Recieved response from alert generator '+gen_name)
		print response.content
		return response.content
	else:
		logging.info("IP address couldn't be retrieved") # Could not connect to database backend to retrieve ip
		response = '{"status":"Database problem"}'
		print response
		return response

#instantiate_alert_generator("HIDS","TCP_MISSING",12133,{"port":"80"})

def profile_alert_generator(gen_name,alert_class,alert_id,args):
	ip = get_ip(gen_name)
        LOG_FILENAME = '/opt/isms/isms/log/client.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,datefmt='%a, %d %b %Y %H:%M:%S',format='%(asctime)s %(levelname)-8s %(message)s\n')
        if ip:
                logging.debug('IP address retrieved '+ip)
                URL = 'http://'+ip+':8080/profile/' # URL of alert generator
                string = '{"generator":"'+gen_name+'","class":"'+alert_class+'","id":"'+str(alert_id)+'","args":"'+str(args)+'"}'
                payload = {"data":string} # type<'dict'>
                logging.info('Sending POST Request to profile alert generator '+gen_name)
                response = requests.post(URL,data=payload)
                logging.info('Recieved response from alert generator '+gen_name)
                print response.content
        else:
                logging.info("IP address couldn't be retrieved") #Could not connect to database backend to retrieve ip
                response = '{"status":"Database problem"}'
                print response		
