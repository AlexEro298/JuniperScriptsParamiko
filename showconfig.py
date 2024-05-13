import netmiko
from sys import argv

#passed arguments
script_name, username, password, host = argv

#connect device
juniper = {'device_type': 'juniper_junos', 'host': f'{host}', 'username': f'{username}',
              'password': f'{password}'}
net_connect = netmiko.ConnectHandler(**juniper)

#show the configuration on the device
show_config = net_connect.send_command('show configuration')
print(show_config)