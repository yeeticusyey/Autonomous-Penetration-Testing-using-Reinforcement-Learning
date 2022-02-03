#!/usr/bin/env python
# coding: utf-8
# %%

# %%


from bs4 import BeautifulSoup
import re
def processNessus(filename):
    with open(filename, 'r') as f:
        data = f.read()
    Bs_data = BeautifulSoup(data, "xml")
    b_item = Bs_data.find_all('ReportHost')

    #print(Bs_data)
    # host ip, report item
    alldata = []
    
    for item in b_item:
        list = []
        list.append(item['name'])
        reported_item = item.find_all('ReportItem')
        reports = []
        temp = []
        
        for x in reported_item:
            if  x.cve != None:
                dicdata = {
                    "pluginName": x['pluginName'],
                    "protocol": x['protocol'],
                    "severity": x['severity'],
                    "description":x.description.get_text(),
                    "plugin_type": x.plugin_type.get_text(),
                    "cve": x.cve.get_text()
                }
                reports.append(dicdata)
            else:      
                if x.risk_factor.get_text() != 'None':
                    dicdata = {
                        "pluginName": x['pluginName'],
                        "protocol": x['protocol'],
                        "severity": x['severity'],
                        "description":x.description.get_text(),
                        "plugin_type": x.plugin_type.get_text(),
                    }
                    reports.append(dicdata)
        list.append(reports)
        alldata.append(list)
    return alldata

#data to extract, reportitem->pluginname, port, protocal. <description>, <plugin_name>, <plugin_modificaiton_date>, <risk_factor>, <script_version>


# %%
