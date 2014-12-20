import imp,random,ConfigParser,subprocess,shlex
from  math import pow

def terminal():
	cmd_line  = 'mkdir /opt/isms/API_new'
	args = shlex.split(cmd_line)
	subprocess.call(args)
	cmd_line = 'cp -avr /opt/isms/API/ /opt/isms/API_new'
	args = shlex.split(cmd_line)
	subprocess.call(args)
	
def generate_API():
	client =  '/opt/isms/API/functions/client.py'
        with open(client,'r') as file:
        	data = file.read()		
	terminal()
	new =  '/opt/isms/API_new/API/functions/client.py'
	rand_key = int(random.random()*pow(10,16))
	with open(new,'w') as file:
                file.write('key = '+str(rand_key)+"\n")
                file.write(data)

generate_API()

