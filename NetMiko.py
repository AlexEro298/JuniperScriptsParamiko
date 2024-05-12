import re
import sys

import netmiko


username = 'netconf'
password = 's123456!'
hosts = ['10.10.3.35']
neighbor_re = re.compile(r'neighbor (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')


for host in hosts:
    junipersrx = {'device_type': 'juniper_junos', 'host': f'{host}', 'username': f'{username}',
                  'password': f'{password}'}
    net_connect = netmiko.ConnectHandler(**junipersrx)
    output = net_connect.send_command('show configuration ---protocols bgp group internal')

    result_file = open(f'bgp received {host}', mode='w')

    for match in neighbor_re.findall(output):
#        text = net_connect.send_command(f'show route receive-protocol bgp {match}')
        text = """
inet.0: 965737 destinations, 2972187 routes (965459 active, 0 holddown, 511 hidden)
  Prefix                  Nexthop              MED     Lclpref    AS path
* 176.126.0.0/19          178.216.152.46                          44172 I
* 176.126.0.0/20          178.216.152.46                          44172 I
* 176.126.12.0/24         178.216.152.46                          44172 I
* 176.126.16.0/20         178.216.152.46                          44172 I
* 195.184.78.0/23         178.216.152.46                          44172 I
* 195.211.236.0/22        178.216.152.46                          44172 I
* 195.211.236.0/23        178.216.152.46                          44172 I
* 195.211.238.0/23        178.216.152.46                          44172 I

inet.3: 9 destinations, 18 routes (9 active, 0 holddown, 0 hidden)

mpls.0: 215 destinations, 215 routes (215 active, 0 holddown, 0 hidden)

inet6.0: 205593 destinations, 455075 routes (205593 active, 0 holddown, 0 hidden)

bgp.l2vpn.0: 62 destinations, 62 routes (62 active, 0 holddown, 0 hidden)

moovi.l2vpn.0: 3 destinations, 3 routes (3 active, 0 holddown, 0 hidden)

cam.l2vpn.0: 2 destinations, 2 routes (2 active, 0 holddown, 0 hidden)

cam2.l2vpn.0: 2 destinations, 2 routes (2 active, 0 holddown, 0 hidden)

ibgp1-vpls.l2vpn.0: 20 destinations, 20 routes (20 active, 0 holddown, 0 hidden)

mng-100g.l2vpn.0: 4 destinations, 4 routes (4 active, 0 holddown, 0 hidden)

mng-cyan.l2vpn.0: 3 destinations, 3 routes (3 active, 0 holddown, 0 hidden)

moscow_mng.l2vpn.0: 3 destinations, 3 routes (3 active, 0 holddown, 0 hidden)

security.l2vpn.0: 3 destinations, 3 routes (3 active, 0 holddown, 0 hidden)

yekt-tyum-x670-27.l2vpn.0: 3 destinations, 3 routes (3 active, 0 holddown, 0 hidden)

reserv-tyum-sur.l2vpn.0: 2 destinations, 2 routes (2 active, 0 holddown, 0 hidden)

global-ix.l2vpn.0: 9 destinations, 9 routes (9 active, 0 holddown, 0 hidden)

tyum-moscow.l2vpn.0: 2 destinations, 2 routes (2 active, 0 holddown, 0 hidden)

piter-ix-helsinki.l2vpn.0: 3 destinations, 3 routes (3 active, 0 holddown, 0 hidden)

piter-ix-kiev.l2vpn.0: 4 destinations, 4 routes (4 active, 0 holddown, 0 hidden)

piter-ix-moscow.l2vpn.0: 4 destinations, 4 routes (4 active, 0 holddown, 0 hidden)

piter-ix-piter.l2vpn.0: 3 destinations, 3 routes (3 active, 0 holddown, 0 hidden)

piter-ix-riga.l2vpn.0: 3 destinations, 3 routes (3 active, 0 holddown, 0 hidden)

piter-ix-tallin.l2vpn.0: 4 destinations, 4 routes (4 active, 0 holddown, 0 hidden)

tyum-nyagan.l2vpn.0: 2 destinations, 2 routes (2 active, 0 holddown, 0 hidden)

stranadev.l2vpn.0: 2 destinations, 2 routes (2 active, 0 holddown, 0 hidden)

piter_baikal_qinq.l2vpn.0: 6 destinations, 6 routes (6 active, 0 holddown, 0 hidden)

l2circuit.0: 8 destinations, 8 routes (8 active, 0 holddown, 0 hidden)

lsdist.0: 139 destinations, 139 routes (139 active, 0 holddown, 0 hidden)
"""
        route_tables = text.split('\n\n')
        inet0_table = list(filter(lambda table: 'inet.0' in table, route_tables))
        if len(inet0_table) > 1:
            print (f'Нашли несколько inet.0 таблиц маршрутизации по адресу {match}. Host: {host}')
            sys.exit(1)
        else:
            print(inet0_table[0])
            result_file.write(f'neighbor {match}')
            result_file.write(inet0_table[0])
            result_file.write('\n\n')
    result_file.close()