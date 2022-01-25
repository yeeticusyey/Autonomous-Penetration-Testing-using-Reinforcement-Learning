#!/usr/bin/env python
# coding: utf-8
# %%


from bs4 import BeautifulSoup
import re
def processdata(filename):
    with open(str(filename), 'r') as f:
        data = f.read()
    Bs_data = BeautifulSoup(data, "xml")
    b_port = Bs_data.find_all('port')
    hosts = Bs_data.find_all('host')
    
    allinformation= []
    for host in hosts:
        list = []
        hostname = host.hostscript
        x = str(hostname).partition("OS:")[2].partition(')')[0] + ')'
        ip = host.address['addr']
        if x == ')':
            print('not found')
            continue
        ports = host.find_all('port')
        temp = []
        for port in ports:  
            temp_port = [port['portid'],port.state['state'],port.service['name']]
            temp.append(temp_port)

        list = [x, ip, temp]
        allinformation.append(list)
    output = []
    for data in allinformation:
        count= []
        for firewall in data[2]:
            if firewall[1] == 'open':
                rule = firewall[2] +', ' + firewall[0] + ', RulePermission.ALLOW'
                count.append(rule)
            else:
                continue
        output.append([data[1], count, data[0]])
    print(output)
    return output




# %%

# %%





# %%

# %%


# %%





# %%




