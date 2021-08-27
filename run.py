import configparser
import paramiko

def main():
	config = configparser.ConfigParser(interpolation=None) # Fix problem with symbols in parameters
	config.read('config.ini')

	###Configuration###
	ssh_username = config['usernames']['ssh_username']
	ssh_password = config['passwords']['ssh_password']
	localhost = config['servers']['localhost']
	server_nw_m2000 = config['servers']['nw_m2000']

	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(hostname=server_nw_m2000, username=ssh_username, password=ssh_password, port=22)

	#Send command
	stdin, stdout, stderr = client.exec_command('ls -1 ~/data/oss/')

	#Result
	data = stdout.read().decode('utf-8') #+ stderr.read()
	print(data)
	client.close()


if __name__ == "__main__":
	 main() # Fix magic problem with AttributeError: 'NoneType' object has no attribute 'time'
