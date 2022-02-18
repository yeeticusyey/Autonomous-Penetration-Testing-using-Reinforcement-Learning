# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# +
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Model a toy Capture the flag exercise

See Jupyter notebook toyctf-simulation.ipynb for an example of
game played on this simulation.
"""
from cyberbattle.simulation import model as m
from cyberbattle.simulation.model import NodeID, NodeInfo, VulnerabilityID, VulnerabilityInfo
from typing import Dict, Iterator, cast, Tuple
import nmapExtract
import Nessusextract
from cyberbattle.simulation import model as m

default_allow_rules = [
    m.FirewallRule("RDP", m.RulePermission.ALLOW),
    m.FirewallRule("SSH", m.RulePermission.ALLOW),
    m.FirewallRule("HTTPS", m.RulePermission.ALLOW),
    m.FirewallRule("HTTP", m.RulePermission.ALLOW)]


# +

def cve_check(data):
    total = []
    for x in data:
        cve = []
        temp = []
        cve.append(x[0])
        for info in x[1]:
            try:
                temp.append(info['cve']) 
            except KeyError:
                   continue
        cve.append(temp)
        total.append(cve) #add node name and cve number
    return total

def vul_handler(name,data): #To add vulnerabilities from nessus
    required= []
    for x in data:
        if x[0] == name:
            required = x[1]
    for info in required: 
        access_level = int(info['severity'])
        if access_level == 0:
            vul_outcome = m.CustomerData()
        elif access_level == 1:
            vul_outcome = m.PrivilegeEscalation(1)
        elif access_level == 2:
            vul_outcome = m.AdminEscalation()
        elif access_level == 3:
            vul_outcome = m.SystemEscalation()
            
        vultype = 'm.VulnerabilityType.{}, '.format(info['plugin_type'].upper())
        vulnames = info['pluginName'].replace(" ", "")
        vulnerabilities = { 
           # if x['plugin_type']
            vulnames : m.VulnerabilityInfo(
            description = info['description'],
            type=eval(vultype)[0], #[0] was used as eval convert vultype into a tuple 
            outcome=vul_outcome, #fake as customer data
            ),
            }
        
        return vulnerabilities



# +


def addnode(nmapfilename, nessusfilename):
    data = nmapExtract.processdata(nmapfilename) # get nmap data process
    nessusoutput = Nessusextract.processNessus(nessusfilename)
    nodeinfo = {}
    node_ids = []
    for x in data:
        x[1] = list(dict.fromkeys(x[1])) 
        rules = ''
        for service in x[1]:
            rules += service
        propertiesa= x[2] #properties from the nmap about the machine
        random = compile(rules,'string', 'eval')
        nodeinfo[str(x[0])] = m.NodeInfo( #node name added
            services= list(eval(random)), # services added
            firewall=m.FirewallConfiguration(incoming=default_allow_rules, # default firewall rules
                                             outgoing=default_allow_rules + [
                                                 m.FirewallRule("su", m.RulePermission.ALLOW),
                                                 m.FirewallRule("sudo", m.RulePermission.ALLOW)]),
            value=10,
            properties=[propertiesa], 
            vulnerabilities= vul_handler(str(x[0]),nessusoutput) #add vulnerbilities with the vul_handler function
        )
        node_ids.append(x[0])
        
    nodeinfo['client'] = m.NodeInfo(
    services=[],
    properties=["CLIENT:Kali"],
    value=0,
    vulnerabilities=dict(
        nmapscan=m.VulnerabilityInfo( #default vulnerbilities running nmap 
            description="Scan the network using Nmap",
            type=m.VulnerabilityType.LOCAL,
            outcome=m.LeakedNodesId(node_ids),
            reward_string="new nodes discovered",
            cost=1.0
        ),
        mimikatz=m.VulnerabilityInfo(  #default vulnerbilities running mimikatz
            description="mimikatz password account crack",
            type=m.VulnerabilityType.REMOTE,
            outcome=m.LeakedCredentials(credentials=[
                    m.CachedCredential(node=node_ids[0],
                                       port="HTTPS",
                                       credential="normaluser")]),
            reward_string="Credentials for normal access",
            cost=1.0
        )),
    agent_installed=True,
    reimagable=False)                      
    cve_info= cve_check(nessusoutput)                
    return nodeinfo, cve_info

node_a, cve_info = addnode('nmapScan.xml',"VA_Network_Scan_7hubkd (1).nessus" ) #Change the Filename to the Nmap scan output



# Environment constants
global_vulnerability_library: Dict[VulnerabilityID, VulnerabilityInfo] = dict([])
def new_environment() -> m.Environment:
    return m.Environment(
        network=m.create_network(node_a),
        vulnerability_library=global_vulnerability_library,
        identifiers=ENV_IDENTIFIERS
    )
ENV_IDENTIFIERS = m.infer_constants_from_nodes(
    cast(Iterator[Tuple[NodeID, NodeInfo]], list(node_a.items())),
    global_vulnerability_library)





