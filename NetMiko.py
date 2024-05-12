import re
import sys
import netmiko

#username and password (authentication data)
username = 'netconf'
password = 's123456!'
host = '10.10.3.35'
#regular expression
neighbor_re = re.compile(r'^neighbor (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', re.MULTILINE)
#neighbor_re = re.compile(r'^\ntype external')
#Connect device
junipersrx = {'device_type': 'juniper_junos', 'host': f'{host}', 'username': f'{username}',
              'password': f'{password}'}
net_connect = netmiko.ConnectHandler(**junipersrx)

#downlinks uplinks v6_uplinks v6_downlinks peers v6_peers need
#group downlikns
#output = net_connect.send_command('show configuration protocols bgp group downlinks')
output = """

"""
print('Group downlinks')
#result_file = open(f'bgp received {host}', mode='w')

for match in neighbor_re.findall(output):
    print(f'IP neighbor: {match}, description:')
    text = net_connect.send_command(f'show route receive-protocol bgp {match}')
    route_tables = text.split('\n\n')
    inet0_table = list(filter(lambda table: 'inet.0' in table, route_tables))
    #if len(inet0_table) > 1:
        #print(f'Нашли несколько inet.0 таблиц маршрутизации по адресу {match}. Host: {host}')
        #sys.exit(1)
    #else:
        #print(inet0_table[0])
        #result_file.write(f'neighbor {match}')
        #result_file.write(inet0_table[0])
        #result_file.write('\n\n')
#result_file.close()
