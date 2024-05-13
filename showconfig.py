import netmiko
from sys import argv

script_name, username, password, host = argv

juniper = {'device_type': 'juniper_junos', 'host': f'{host}', 'username': f'{username}',
              'password': f'{password}'}
net_connect = netmiko.ConnectHandler(**juniper)
show_config = net_connect.send_command('show configuration')
print(f'{script_name},{username},{password},{host}')
print(show_config)