import paramiko, time


max_buffer = 65535
username = 'netconf'
password = 's123456!'
hosts = ['10.10.3.35']


for host in hosts:
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(f'{host}', username = f'{username}', password = f'{password}', look_for_keys = False, allow_agent = False)

    stdin, stdout, stderr = connection.exec_command('show configuration protocols bgp',65535)
    print(stdout.read().decode())

    # stdin, stdout, stderr = connection.exec_command('show version', 65535)
    # print(stdout.read().decode())

    # channel = connection.invoke_shell()
    # time.sleep(5)
    # stdin = channel.makefile_stdin('wb')
    # stdout = channel.makefile("r", 65000)
    # stderr = channel.makefile_stderr()
    # stdin.write('show version\n')
    # stdin.write('show configuration\n')
    # time.sleep(15)
    # print(channel.recv(65000).decode())
