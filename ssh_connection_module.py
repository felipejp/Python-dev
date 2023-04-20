import paramiko

cmd_to_execute = "display current-configuration"

def get_configuration(IP):

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(IP, username="fbova", password="arsat123")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
    except Exception as error:
        print(str(error))

    return_string = ssh_stdout.read().decode()
    ssh.close()
    
    return(return_string)

