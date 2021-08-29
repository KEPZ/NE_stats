import configparser
import paramiko
from stat import S_ISDIR, S_ISREG

# autopep8 -i filename.py


def main():
    # Fix problem with symbols in parameters
    config = configparser.ConfigParser(interpolation=None)
    config.read('config.ini')

    ###Configuration###
    ssh_username = config['usernames']['ssh_username']
    ssh_password = config['passwords']['ssh_password']
    localhost = config['servers']['localhost']
    server_nw_m2000 = config['servers']['nw_m2000']
    localpath = config['paths']['localpath']
    reports = config['paths']['reports']
    scripts = config['paths']['scripts']
    tasks = config['paths']['tasks']

    # SSH connection
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=server_nw_m2000,
                       username=ssh_username, password=ssh_password, port=22)
    except (paramiko.ssh_exception.NoValidConnectionsError):
        print('Error: Remote host {} is unavailable or bad credentials'.format(
            server_nw_m2000,))
        exit(1)
    except (paramiko.ssh_exception.AuthenticationException):
        print('Error: Bad credentials')
        exit(1)

    # Send command
    stdin, stdout, stderr = client.exec_command('pwd; tree data/oss/')

    # Result
    data = stdout.read().decode('utf-8')  # + stderr.read()
    print(data)

    # SFTP connection
    ftp_client = client.open_sftp()
#	print(dir(ftp_client))
#	print(dir(client))
    files = []  # List of files
    zipdir = scripts
#    for entry in ftp_client.listdir_attr(zipdir):
#        mode = entry.st_mode
# if S_ISDIR(mode):
##            print(zipdir + entry.filename + " is folder")
#        if S_ISREG(mode):
##            print(zipdir + entry.filename + " is file")
#            files.append(zipdir + entry.filename)
##   print(' '.join(files))
    sin, serr, sout = client.exec_command(
        'tar cf ' + zipdir + 'NE_stats.tar' + ' -C ' + zipdir + ' .')
# Check archive: tar -tf NE_stats.tar
    #print(serr.read().decode('utf-8'), sout.read())
    ftp_client.get(scripts + 'run.sh', '/tmp/scr.sh')
    ftp_client.close()
    client.close()


if __name__ == "__main__":
    main()  # Fix magic problem with AttributeError: 'NoneType' object has no attribute 'time'
