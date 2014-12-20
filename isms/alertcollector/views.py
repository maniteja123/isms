from alertcollector.models import Alertgenerator,Alertgroup,Alertclass
from alertcollector.serializers import GeneratorSerializer,GroupSerializer,ClassSerializer
from django.http import HttpResponse
import json,ast,imp,django,logging,os
#Create your views here.
dir =  os.path.dirname(os.path.dirname(__file__))

class JSONResponse(HttpResponse):

    def __init__(self,data,**kwargs):
        content = json.dumps(data)
        kwargs['content_type']='application/json'
        super(JSONResponse,self).__init__(content,**kwargs)

         
def add_generator(request):  # Register the alert generator
	response={}      
	LOG_FILENAME = dir+'/log/server.log'
	logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,datefmt='%a, %d %b %Y %H:%M:%S',format='%(asctime)s %(levelname)-8s %(message)s\n')
	if request.method=='POST':  # check if it is 'POST' request
		logging.info('Received POST request for registering generator')
        	info = request.POST.get("data")         # type <'unicode'>
		try:
			logging.debug('Decoding JSON '+str(info))
			data = json.loads(info)               # type<'dict'>
		except Exception :                # JSON not decodable
			logging.exception('JSON not parsed properly')
			response['status']='JSON format not correct'
			response['code']=401
		else:
			logging.debug('JSON decoded and retrieved parameters '+str(data))
		       	gen_name = data["name"] # getting parameters from a dict
		       	gen_author = data["author"]
 		        gen_ip =  data["ip"]
                        gen_key = int(data["key"])
		        try:
				logging.debug('Checking with the alert generator models in the database')
		        	generator = Alertgenerator.objects.get_or_create(alert_gen_name=gen_name, alert_gen_author=gen_author,alert_gen_ip=gen_ip,alert_gen_key=gen_key)
			except django.db.OperationalError :
				logging.exception('Database not running on the server')
				response['status']='Unable to connect to the database' # database not running
				response['code']=501
			else:
			        if generator[1]:
					logging.info('New generator registered '+gen_name)
					generator[0].deleted = False
					generator[0].save() # reset the deleted flag
					response['status']="Generator successfully registered"  # New generator registered
					response['code']=200
			        else:
					if generator[0].alert_gen_ip == gen_ip and generator[0].alert_gen_key == gen_key:
						if generator[0].deleted:
							logging.info('Already existing but deleted generator '+gen_name)
							generator[0].deleted = False #Reset the deleted flag
							generator[0].save()
							response['status']="Generator already exists but was deleted"   # Generator was deleted
						else :
							logging.info('Already registered genererator')
							response['status']="Generator already registered" # Generator already registered
						response['code']=200
		                        elif generator[0].alert_gen_ip != gen_ip:
						logging.error('IP address not matching REG: '+str(generator[0].alert_gen_ip)+' GIVEN: '+str(gen_ip))
                		                response['status']="Generator exists but IP configuration not matching"  # IP address not matching with the registered one
                                		response['code']=402
		                        elif generator[0].alert_gen_key != gen_key:
						logging.error('Key not correct')
                	        	        response['status']="Generation error but Authentication error" # Key not matching
                        	       		response['code']=402
	else:
		logging.warning('Request not sent by client through POST')
		response['status']="There was some error in request sent"   # Request was not properly sent
		response['code']=400
	return JSONResponse(response)


def update_generator(request):       # Update an existing alert generator  
	response = {}
	LOG_FILENAME = dir+'/log/server.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,datefmt='%a, %d %b %Y %H:%M:%S',format='%(asctime)s %(levelname)-8s %(message)s\n')
	if request.method == 'POST':
		logging.info('Received POST request for updating alert generator')
		info = request.POST.get("data")         # type <'unicode'>
		try:
 	       		logging.debug('Decoding JSON '+str(info))
			data = json.loads(info)               # type<'dict'>
		except Exception:
			logging.exception('JSON not parsed properly')
			response['status']='JSON format not correct'  # JSON not decodable
                	response['code']=401
		else:
			logging.debug('JSON decoded and retrieved parameters '+str(data))
	                gen_name = data["name"] # getting parameters from a dict
        	        gen_author = data["author"]
	  	        gen_ip =  data["ip"]
         	        gen_key = int(data["key"])
		        new = ast.literal_eval(data["args"])
		try:
			logging.debug('Checking with the alert generator models in the database')
		        generator = Alertgenerator.objects.get(alert_gen_name=gen_name, alert_gen_author=gen_author)
		except django.db.OperationalError:
			logging.exception('Database not running on the server')
  			response['status']='Unable to connect to the database' # database not running
                        response['code']=501
		except Alertgenerator.DoesNotExist :
			logging.info('No registered alert generator has name '+gen_name)
	                response['status'] = "Any corresponding alert generator doesn't exist"  # Alert generator not found in database
        	        response['code']=200
		else:
		        if generator.alert_gen_ip == gen_ip and generator.alert_gen_key == gen_key and not generator.deleted:
        	       		for key in new:
					if key=='name':
						generator.alert_gen_name = new["name"]
					elif key=='author':
						generator.alert_gen_author = new["author"]
				generator.save() # save the generator after modifying attributes
				logging.info('Successfully updated the alert generator '+gen_name)
				response['status'] = "Successfully modified the alert generator" # modified the attributes of the generator
				response['code']=200
	    		elif generator.alert_gen_ip != gen_ip:
				logging.error('IP address not matching REG: '+str(generator.alert_gen_ip)+' GIVEN: '+str(gen_ip))
		       	        response['status']="IP configuration not matching"  # IP address not matching with the registered one
				response['code']=402
		  	elif generator.alert_gen_key != gen_key:
				logging.error('Key not correct')
        		        response['status']="Authentication error" # Key not matching
				response['code']=402
			elif generator.deleted:
				logging.info('alert generator wasdeleted') #alert generator was deleted
				response['status'] = "alert generator was deleted"
				response['code']=200
	else:
		logging.warning('Request not sent by client through POST')
		response['status']="There was some error in request sent" # Request was not properly sent
	        response['code']=400	
	return JSONResponse(response)

def delete_generator(request):
	response = {}
	LOG_FILENAME = dir+'/log/server.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,datefmt='%a, %d %b %Y %H:%M:%S',format='%(asctime)s %(levelname)-8s %(message)s\n')
	if request.method=='POST':
		logging.info('Received POST request for deleting alert generator')
	    	info = request.POST.get("data")         # type <'unicode'>
		try:
		    	logging.debug('Decoding JSON '+str(info))
			data = json.loads(info)               # type<'dict'>
		except Exception:
			logging.exception('JSON not parsed properly')
			response['status']='JSON format not correct'  # JSON not decodable
                        response['code']=401
		else:
			logging.debug('JSON decoded and retrieved parameters '+str(data))
			gen_name = data["name"] # getting parameters from a dict
			gen_author = data["author"]
			gen_ip =  data["ip"]
	      		gen_key = int(data["key"])
			try:
				logging.debug('Checking with the alert generator models in the database')
				generator = Alertgenerator.objects.get(alert_gen_name=gen_name, alert_gen_author=gen_author)
			except Alertgenerator.DoesNotExist:
				logging.info('No registered alert generator has name '+gen_name)
                        	response['status']="Any corresponding alert generator doesn't exist" # No alert generator with the given name is registered
	                        response['code']=200
			except django.db.OperationalError :	
				logging.exception('Database not running on the server')
				response['status']='Unable to connect to the database' # database not running
	                        response['code']=501
			else:
				if generator.alert_gen_ip == gen_ip and generator.alert_gen_key == gen_key and not generator.deleted:
					generator.deleted = True
					generator.save()
					logging.info('Successfully deleted  alert generator '+generator.alert_gen_name)
				  	response['status'] = "Successfully deleted the alert generator" # set the 'deleted' flag
					response['code']=200
				elif generator.alert_gen_ip != gen_ip:
					logging.error('IP address not matching REG: '+str(generator.alert_gen_ip)+' GIVEN: '+str(gen_ip))
			                response['status']="IP configuration not matching" # IP address not matching with the registered one
					response['code']=402
			        elif generator.alert_gen_key != gen_key:
					logging.error('Key not correct')
			                response['status']="Authentication error"  # Key not matching
					response['code']=402
				elif generator.deleted:
                                	logging.info('alert generator was deleted') #alert generator was deleted
	                                response['status'] = "alert generator was deleted"
        	                        response['code']=200

	else:
		logging.warning('Request not sent by client through POST')
		response['status']="There was some error in request sent" # Request was not properly sent
                response['code']=400
	return JSONResponse(response)

def verify_generator(request):
	response = {}
	LOG_FILENAME = dir+'/log/server.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,datefmt='%a, %d %b %Y %H:%M:%S',format='%(asctime)s %(levelname)-8s %(message)s\n')
	if request.method=='POST':
		logging.info('Received POST request for verifying alert generator') 
	        info = request.POST.get("data")         # type <'unicode'>
		try:
			logging.debug('Decoding JSON '+str(info))
		        data = json.loads(info)               # type<'dict'>
		except Exception:
			logging.exception('JSON not parsed properly')
                        response['status']='JSON format not correct'  # JSON not decodable
                        response['code']=401
		else:
			logging.debug('JSON decoded and retrieved parameters '+str(data))
		        gen_name = data["name"] # getting parameters from a dict
        		gen_author = data["author"]
			gen_ip = data["ip"]
			gen_key = int(data["key"])
			try :
				logging.debug('Checking with the alert generator models in the database')
				generator = Alertgenerator.objects.get(alert_gen_name=gen_name, alert_gen_author=gen_author)
			except Alertgenerator.DoesNotExist:
				logging.info('No registered alert generator has name '+gen_name)
        	                response['status']="Any corresponding alert generator doesn't exist" # no alert generator with given name registered
                                response['code']=200
                        except django.db.OperationalError :
                                logging.exception('Database not running on the server')
				response['status']='Unable to connect to the database' # database not running
                                response['code']=501
			else:
				if generator.alert_gen_ip == gen_ip and generator.alert_gen_key == gen_key and not generator.deleted:
					logging.info('Already registered alert generator has name '+gen_name)
			                response['status'] = "Already registered"  # alert generator already registered
					response['code']=200
			        elif generator.alert_gen_ip != gen_ip:
					logging.error('IP address not matching REG: '+str(generator.alert_gen_ip)+' GIVEN: '+str(gen_ip))
			                response['status']="IP configuration not matching" # IP address not matching with the registered one
					response['code']=402
			        elif generator.alert_gen_key != gen_key:
					logging.error('Key not correct')
			                response['status']="Authentication error" #key not matching
					response['code']=402
				elif generator.deleted:
                	                logging.info('alert generator wasdeleted') #alert generator was deleted
	                                response['status'] = "alert generator was deleted"
        	                        response['code']=200

	else:
		logging.warning('Request not sent by client through POST')
                response['status']="There was some error in request sent" # Request was not properly sent
                response['code']=400
	return JSONResponse(response)

def add_group(request): 
	response = {}
	LOG_FILENAME = dir+'/log/server.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,datefmt='%a, %d %b %Y %H:%M:%S',format='%(asctime)s %(levelname)-8s %(message)s\n')
	if request.method == 'POST': 
		logging.info('Received POST request for registering alert group')
    		info = request.POST.get("data")         # type <'unicode'>
		try:
			logging.debug('Decoding JSON '+str(info))
			data = json.loads(info)               # type<'dict'>	
		except Exception:
			logging.exception('JSON not parsed properly')
			response['status']='JSON format not correct'  # JSON not decodable
                        response['code']=401
		else:
			logging.debug('JSON decoded and retrieved parameters '+str(data))
			group_name = data["name"] # getting parameters from a dict
			group_desc = data["description"]
			group_gen = data["generator"]
			group_author = data["author"]
			group_key = int(data["key"])
			group_ip = data["ip"]
			try:
				logging.debug('Checking with the alert generator models in the database')
				generator = Alertgenerator.objects.get(alert_gen_name=group_gen,alert_gen_author=group_author)  
			except django.db.OperationalError:
	                        logging.exception('Database not running on the server')
				response['status']='Unable to connect to the database' # database not running
        	                response['code']=501
			except Alertgenerator.DoesNotExist:
				logging.info('No registered alert generator has name '+group_gen)
				response['status']="Alert generator doesn't exist" # corresponding generator not registered
                                response['code']=200
			else:	
				if generator.alert_gen_ip == group_ip and generator.alert_gen_key == group_key and not generator.deleted:
					logging.debug('Checking with the alert group models in the database')
					group = Alertgroup.objects.get_or_create(alert_group_name=group_name,alert_group_description=group_desc,alert_gen=generator)  # no need to catch OperatonalError since would have been already caught
					if group[1]:
						logging.info('Successfully registered alert group '+group_name)
						group[0].deleted = False
						group[0].save() # Reset the deleted flag
						response['status']="Alertgroup successfully registered" #New alert group is registered
					else:
						if group[0].deleted:
                                                        logging.info('Already existing but deleted group '+group_name)
                                                        group[0].deleted = False #Reset the deleted flag
                                                        group[0].save()
                                                        response['status']="Group already exists but was deleted"   # Group was deleted
                                                else :
                                                        logging.info('Already registered group')
                                                        response['status']="Group already registered" # Group already registered
                                                response['code']=200

						logging.info('Alreadyregistered alert group '+group_name)
						group[0].deleted = False
						group[0].save()	# Reset the deleted flag
					        response['status']="Alertgroup already exists" # Already registered alert group
					response['code']=200
				elif generator.alert_gen_ip != group_ip:
					logging.error('IP address not matching REG: '+str(generator.alert_gen_ip)+' GIVEN: '+str(group_ip))
				        response['status']="IP configuration not matching" # IP address not matching with the registered one
					response['code']=402
			        elif generator.alert_gen_key != group_key:
					logging.error('Key not correct')
					response['status']="Authentication error"  # key not matching
					response['code']=402
				elif generator.deleted:
	                                logging.info('alert generator was deleted') #alert generator was deleted
        	                        response['status'] = "alert generator was deleted"
                	                response['code']=200

	else:
		logging.warning('Request not sent by client through POST')
	        response['status']="There was some error in request sent" # Request was not properly sent
                response['code']=400
	return JSONResponse(response)

def verify_group(request):
	response = {}
	LOG_FILENAME = dir+'/log/server.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,datefmt='%a, %d %b %Y %H:%M:%S',format='%(asctime)s %(levelname)-8s %(message)s\n')
	if request.method == 'POST':
		logging.info('Received POST request for verifying alert group')
	        info = request.POST.get("data")         # type <'unicode'>
		try:
			logging.debug('Decoding JSON '+str(info))
		        data = json.loads(info)               # type<'dict'>
		except Exception:
			logging.exception('JSON not parsed properly')
			response['status']='JSON format not correct'  # JSON not decodable
                        response['code']=401
		else:
			logging.debug('JSON decoded and retrieved parameters '+str(data))
		        group_name = data["name"] # getting parameters from a dict
		        group_desc = data["description"]
        		group_gen = data["generator"]
	       		group_author = data["author"]
			group_key = int(data["key"])
                        group_ip = data["ip"]
			try:	
				logging.debug('Checking with the alert generator models in the database')
				generator = Alertgenerator.objects.get(alert_gen_name=group_gen,alert_gen_author=group_author) 
			except  django.db.OperationalError:
                                logging.exception('Database not running on the server')
				response['status']='Unable to connect to the database' # database not running
                                response['code']=501
                        except Alertgenerator.DoesNotExist:
				logging.info('No registered alert generator has name '+group_gen)
                                response['status']="Alert generator doesn't exist" # corresponding generator not registered
	                        response['code']=200
			else:
				if generator.alert_gen_ip == group_ip and generator.alert_gen_key == group_key and not generator.deleted:
					try:
						logging.debug('Checking with the alert group models in the database')
						groups = Alertgroup.objects.get(alert_group_name=group_name,alert_group_description=group_desc,alert_gen=generator)	# no need to catch OperatonalError since would have been already caught
					except Alertgroup.DoesNotExist:
						logging.info('No registered alert group has name '+group_name+' under alert generator '+group_gen)
						response['status']="No such group exists under this generator" # alert group not under this generator
	                                        response['code']=200
					else:
						logging.info('Successfully verified alert group '+group_name)
						response['status']="Already exists" # It is already registered
						response['code']=200
				elif generator.alert_gen_ip != group_ip:
					logging.error('IP address not matching REG: '+str(generator.alert_gen_ip)+' GIVEN: '+str(group_ip))
		        	        response['status']="IP configuration not matching" # IP address not matching with the registered one
					response['code']=402
				elif generator.alert_gen_key != group_key:
					logging.error('Key not correct')
        		        	response['status']="Authentication error"  # key not matching
					response['code']=402
                                elif generator.deleted:
                                        logging.info('alert generator was deleted') #alert generator was deleted
                                        response['status'] = "alert generator was deleted"
                                        response['code']=200

	else:
		logging.warning('Request not sent by client through POST')
		response['status']="There was some error in reqeust sent" # Request was not properly sent
		response['code']=400
	return JSONResponse(response)

def delete_group(request):
	response = {}
	LOG_FILENAME = dir+'/log/server.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,datefmt='%a, %d %b %Y %H:%M:%S',format='%(asctime)s %(levelname)-8s %(message)s\n')
	if request.method == 'POST':
		logging.info('Received POST request for deleting alert group')
		info = request.POST.get("data")         # type <'unicode'>
		try:
			logging.debug('Decoding JSON '+str(info))
	                data = json.loads(info)               # type<'dict'>
        	except Exception:
			logging.exception('JSON not parsed properly')
			response['status']='JSON format not correct'  # JSON not decodable
	                response['code']=401
		else:
			logging.debug('JSON decoded and retrieved parameters '+str(data))
		        group_name = data["name"] # getting parameters from a dict
        	        group_desc = data["description"]
			group_gen = data["generator"]
		        group_author = data["author"]
		        group_key = int(data["key"])
	       		group_ip = data["ip"]
			try:
				logging.debug('Checking with the alert generator models in the database')
				generator = Alertgenerator.objects.get(alert_gen_name=group_gen,alert_gen_author=group_author) 
			except  django.db.OperationalError:
                                logging.exception('Database not running on the server')
				response['status']='Unable to connect to the database' # database not running
                                response['code']=501
                        except Alertgenerator.DoesNotExist:
				logging.info('No registered alert generator has name '+group_gen)
                                response['status']="Alert generator doesn't exist" # corresponding generator not registered
                                response['code']=200
			else:
			        if generator.alert_gen_ip == group_ip and generator.alert_gen_key == group_key and not generator.deleted:
        				try:
						logging.debug('Checking with the alert group models in the database')
                				group =  Alertgroup.objects.get(alert_group_name=group_name,alert_group_description=group_description,alert_gen=generator) # no need to catch OperatonalError since would have been already caught
                                        except Alertgroup.DoesNotExist:
						logging.info('No registered alert group has name '+group_name+' under alert generator '+group_gen)	
                                                response['status']="No such group exists under this generator" # alert group not under this generator
                                                response['code']=200
					else:
						group.delete = True
						group.save() # set the deleted flag
						logging.info('Successfully deleted alert group '+group_name)
						response['status'] = "Alertgroup successfully deleted"
						response['code']=200
				elif generator.alert_gen_ip != group_ip:
					logging.error('IP address not matching REG: '+str(generator.alert_gen_ip)+' GIVEN: '+str(group_ip))
        		        	response['status']="IP configuration not matching" # IP address not matching with the registered one
					response['code']=200
			        elif generator.alert_gen_key != group_key:
					logging.error('Key not correct')
				        response['status']="Authentication error"  # key not matching
					response['code']=200
                                elif generator.deleted:
                                        logging.info('alert generator was deleted') #alert generator was deleted
                                        response['status'] = "alert generator was deleted"
                                        response['code']=200					
	else:
		logging.warning('Request not sent by client through POST')
		response['status']="There was some error in reqeust sent" # Request was not properly sent
                response['code']=400
	return JSONResponse(response)

def update_group(request):  
	response = {}
	LOG_FILENAME = dir+'/log/server.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,datefmt='%a, %d %b %Y %H:%M:%S',format='%(asctime)s %(levelname)-8s %(message)s\n')
        if request.method == 'POST':
		logging.info('Received POST request for updating alert group')
                info = request.POST.get("data")         # type <'unicode'>
		try:
			logging.debug('Decoding JSON '+str(info))
			data = json.loads(info)               # type<'dict'>
		except Exception:	
			logging.exception('JSON not parsed properly')
			response['status']='JSON format not correct'  # JSON not decodable
                        response['code']=401
		else:
			logging.debug('JSON decoded and retrieved parameters '+str(data))
			group_name = data["name"] # getting parameters from a dict
        	        group_desc = data["description"]
	                group_gen = data["generator"]
        	        group_author = data["author"]
	                group_key = int(data["key"])
	                group_ip = data["ip"]
			new = ast.literal_eval(data["args"])
			try:
				logging.debug('Checking with the alert generator models in the database')
				generator = Alertgenerator.objects.get(alert_gen_name=group_gen,alert_gen_author=group_author) 
	                except django.db.OperationalError:
				logging.exception('Database not running on the server')
				response['status']='Unable to connect to the database' # database not running
                	        response['code']=501
	                except Alertgenerator.DoesNotExist:
				logging.info('No registered alert generator has name '+group_gen)
        	        	response['status']="Alert generator doesn't exist" # corresponding generator not registered
                	        response['code']=200
			else:
        	                if generator.alert_gen_ip == group_ip and generator.alert_gen_key == group_key and not generator.deleted:
                	                try:
                        	                group =  Alertgroup.objects.get(alert_group_name=group_name,alert_group_description=group_desc,alert_gen=generator) # no need to catch OperatonalError since would have been already caught
        	                        except Alertgroup.DoesNotExist:
						logging.info('No registered alert group has name '+group_name+' under alert generator '+group_gen)
                	                        response['status']="No such group exists under this generator" # alert group not under this generator
                        	                response['code']=200
					else:
						for key in new:
							if key=='name':
								group.alert_group_name = new["name"]
							elif key=='description':
								group.alert_group_description = new["description"]
						group.save() #save the group after modifying the attributes
						logging.info('Successfully updated alert group '+group_name)
                	                        response['status'] = "Alertgroup successfully modified"
						response['code']=200
	                        elif generator.alert_gen_ip != group_ip:
					logging.error('IP address not matching REG: '+str(generator.alert_gen_ip)+' GIVEN: '+str(group_ip))
        	                        response['status']="IP configuration not matching" # IP address not matching with the registered one
					response['code']=402
	                        elif generator.alert_gen_key != group_key:
					logging.error('Key not correct')
        	                        response['status']="Authentication error"  # key not matching
					response['code']=402
                                elif generator.deleted:
                                        logging.info('alert generator was deleted') #alert generator was deleted
                                        response['status'] = "alert generator was deleted"
                                        response['code']=200
	else:
		logging.warning('Request not sent by client through POST')
     		response['status']="There was some error in request sent" # Request was not properly sent
		response['code']=400
        return JSONResponse(response)

def add_class(request):
	response = {}
	LOG_FILENAME = dir+'/log/server.log'
        logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,datefmt='%a, %d %b %Y %H:%M:%S',format='%(asctime)s %(levelname)-8s %(message)s\n')
	if request.method == 'POST':		
		logging.info('Received POST request for registering alert class')
		info = request.POST.get("data")         # type <'unicode'>
		try:
			logging.debug('Decoding JSON '+str(info))
	                data = json.loads(info)               # type<'dict'>
		except Exception:
			logging.exception('JSON not parsed properly')
			response['status']='JSON format not correct'  # JSON not decodable
                        response['code']=401
		else:
			logging.debug('JSON decoded and retrieved parameters '+str(data))
	                class_name = data["name"]
			class_desc = data["description"]
			class_help = data["help"]
			class_syntax = data["syntax"]
			class_filter = data["filter"]
			class_parent = data["parent"]
			class_group = data["group"]
			class_ip = data["ip"]
			class_key = int(data["key"])
			try:
				logging.debug('Checking with the alert group models in the database')
				group = Alertgroup.objects.get(alert_group_name=class_group)
			except django.db.OperationalError:
                        	logging.exception('Database not running on the server')
				response['status']='Unable to connect to the database' # database not running
                                response['code']=501
               	        except Alertgroup.DoesNotExist:
				logging.info('No registered alert group has name '+class_group)
                        	response['status']="No such group exists" # alert group not exists
                                response['code']=200
			else:
				generator  = group.alert_gen
				if generator.alert_gen_ip == class_ip and generator.alert_gen_key == class_key and not generator.deleted and not group.deleted:
					if class_filter=='':
						is_filter=False
					else:
						is_filter=True
					logging.debug('Creating an alert class entry in the database')
					alert_class = Alertclass.objects.create(alert_class_name=class_name,alert_class_description=class_desc,alert_class_help=class_help,alert_class_syntax=class_syntax,alert_class_filter_syntax=class_filter,alert_class_parent=class_parent,alert_group=group,is_filter=is_filter)
					logging.info('Successfully registered alert class '+class_name)
					response['status'] = "Alertclass registered" # New alert class registered
					response['code']=200
				elif generator.alert_gen_ip != class_ip:
					logging.error('IP address not matching REG: '+str(generator.alert_gen_ip)+' GIVEN: '+str(class_ip))
                                        response['status']="IP configuration not matching" # IP address not matching with the registered one
                                        response['code']=402
                                elif generator.alert_gen_key != class_key:
					logging.error('Key not correct')
                                        response['status']="Authentication error"  # key not matching
                                        response['code']=402
                                elif generator.deleted:
                                        logging.info('alert generator was deleted') #alert generator was deleted
                                        response['status'] = "alert generator was deleted"
                                        response['code']=200
                                elif group.deleted:
                                        logging.info('alert group was deleted') #alert group was deleted
                                        response['status'] = "alert group was deleted"
                                        response['code']=200

	else:
		logging.warning('Request not sent by client through POST')
		response['status'] = "There was some error in request sent" # Request was not properly sent
                response['code']=400
	return JSONResponse(response)
