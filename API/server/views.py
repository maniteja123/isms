import json,imp,ConfigParser,ast,os
from django.http import HttpResponse
# Create your views here.
dir = os.path.dirname(os.path.dirname(__file__))

class JSONResponse(HttpResponse):	
	
	def __init__(self, data, **kwargs):
		content = json.dumps(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse,self).__init__(content,**kwargs)

def instance_create(request):
	response = {}
	if request.method == 'POST':
		print "hi"
		info = request.POST.get('data')  # <type 'unicode'>
		print info
		try:
			data = json.loads(info)		# < type 'dict'>
			print data
		except Exception:
			response['status']='JSON format not correct'
                	response['code']=401
		else:
			generator = data['generator'] # get items from dict
			alert_class = data['class']
			alert_id = data['id']
			args = ast.literal_eval(data['args']) # removing quotes to parse the string to dict
			config = ConfigParser.RawConfigParser()
			config.read(dir+'/config/client/client_conf.ini')
			path = config.get('client','functions')
			function = imp.load_source("client_func",path)
			response = function.alert_instance_creation(alert_class,alert_id,args)
			response['code']=200
	else:
		response['status']="There was some error in reqeust sent" # Request was not properly sent
		response['code']=400
	return JSONResponse(response)

def profile_alert(request):
	response = {}
        if request.method == 'POST':
                info = request.POST.get('data')  # <type 'unicode'>
                try:
                        data = json.loads(info)         # < type 'dict'>
                except Exception:
                        response['status']='JSON format not correct'
                        response['code']=401
                else:
                        generator = data['generator'] # get items from dict
                        alert_class = data['class']
                        alert_id = data['id']
                        args = ast.literal_eval(data['args']) # removing quotes to parse the string to dict
                        for keys in new:
                                print keys
                        config = ConfigParser.RawConfigParser()
                        config.read(dir+'/config/client/client_conf.ini')
                        path = config.get('client','functions')
                        function = imp.load_source("client_func",path)
                        response = function.alert_profile(alert_class,alert_id,args)
                        response['code']=200
        else:
                response['status']="There was some error in reqeust sent" # Request was not properly sent
                response['code']=400
        return JSONResponse(response)

  
   
    







