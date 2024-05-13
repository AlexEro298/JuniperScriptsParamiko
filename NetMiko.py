import re
from sys import argv
import netmiko

#passed arguments for console
script_name, username, password, host = argv

#name group bgp
group_ipv4 = ['uplinks', 'downlinks', 'peers']
group_ipv6 = ['v6_uplinks', 'v6_downlinks', 'v6_peers']

#regular expression
neighbor_ipv4_re = re.compile(r'^neighbor (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', re.MULTILINE)
neighbor_ipv6_re = re.compile(r'^neighbor (([0-9a-fA-F]{0,4}:){1,7}[0-9a-fA-F]{0,4})', re.MULTILINE)

#Connect device
juniper = {'device_type': 'juniper_junos', 'host': f'{host}', 'username': f'{username}',
              'password': f'{password}'}
network_connect = netmiko.ConnectHandler(**juniper)



#IPv4 group
for name_group_v4 in group_ipv4:
    print(f'Group {name_group_v4}:')
    show_config_bgp_group = network_connect.send_command(f'show configuration protocols bgp group {name_group_v4}')
    for ip_neighboor in neighbor_ipv4_re.findall(show_config_bgp_group):
        print(f'IP neighbor: {ip_neighboor}')
        show_route_receive_protocol_bgp = network_connect.send_command(f'show route receive-protocol bgp {ip_neighboor}')
        route_tables = show_route_receive_protocol_bgp.split('\n\n')
        inet0_table = list(filter(lambda table: 'inet.0' in table, route_tables))
        print(str(inet0_table[0])[1:] + '\n\n')

#IPv6 group
for name_group_v6 in group_ipv6:
    print(f'Group {name_group_v6}:')
    show_config_bgp_group = network_connect.send_command(f'show configuration protocols bgp group {name_group_v6}')
    for ip_neighboor in neighbor_ipv4_re.findall(show_config_bgp_group):
        print(f'IP neighbor: {ip_neighboor}')
        show_route_receive_protocol_bgp = network_connect.send_command(f'show route receive-protocol bgp {ip_neighboor}')
        route_tables = show_route_receive_protocol_bgp.split('\n\n')
        inet0_table = list(filter(lambda table: 'inet6.0' in table, route_tables))
        print(str(inet0_table[0])[1:] + '\n\n')