
import datetime
import wget 
import gzip
import shutil
import sqlite3
import os
import pandas as pd
import json


try:
	conn = sqlite3.connect('nvd.db')
	print("Opened database successfully")

except Exception as e:
	print("Error during connection: ", str(e))


i = 2002;
#The oldest NVD database is in 2002

current_date = datetime.date.today()
year = current_date.year

# variable year indicates the current year

while i<=year:	
	info = f"Beginning downloading NVD database of year {i}"
	print(info)
	#download (i) year's nvd database
	nvd_url = "https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{0}.json.gz".format(i)
	wget.download(nvd_url)
	#gunzip the nvd database in the current directory
	with gzip.open('nvdcve-1.1-{0}.json.gz'.format(i), 'rb') as f_in:
		with open('nvdcve-1.1-{0}.json'.format(i), 'wb') as f_out:
			shutil.copyfileobj(f_in, f_out)
			#removes the unecessary gz file
			os.remove('nvdcve-1.1-{0}.json.gz'.format(i))

	#create a dataframe from the JSON data
	df = pd.read_json('nvdcve-1.1-{0}.json'.format(i))
	#print(df)
	mysql_dict = {'CVE_ID':[],'description':[],'vectorString':[],'attackVector':[],'attackComplexity':[],'privilegesRequired':[],'userInteraction':[],'confidentialityImpact':[],'integrityImpact':[],'availabilityImpact':[],'baseScore':[]}
	#Create a dictionary to hold the necessary information before loading into data frame
	counter = 0
	for index, row in df.iterrows():
		cve = row["CVE_Items"]
		cve_id = cve["cve"]["CVE_data_meta"]["ID"]
		mysql_dict["CVE_ID"].append(cve_id)
		cve_d = cve["cve"]["description"]["description_data"][0]["value"]
		mysql_dict["description"].append(cve_d)

		cve_list = ['vectorString', 'attackVector', 'attackComplexity', 'privilegesRequired', 'userInteraction', 'confidentialityImpact', 'integrityImpact', 'availabilityImpact','baseScore']

		try:
			for x in cve_list:
				mysql_dict[x].append(cve["impact"]["baseMetricV3"]["cvssV3"][x])

		except KeyError:
			for x in cve_list:
				mysql_dict[x].append('')
		#Not all CVEs would have an impact, therefore those will be having a blank in the table

	sqldf = pd.DataFrame(mysql_dict, columns=['CVE_ID','description','vectorString', 'attackVector', 'attackComplexity', 'privilegesRequired', 'userInteraction', 'confidentialityImpact', 'integrityImpact', 'availabilityImpact','baseScore'])
	#Loading everything into data frame
	c = conn.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS nvd (CVE_ID, description, vectorString, attackVector, attackComplexity, privilegesRequired, userInteraction, confidentialityImpact, integrityImpact, availabilityImpact,baseScore)')
	conn.commit()
	#Create the sqlite3 table if it does not exist

	if i == 2002:
	
		sqldf.to_sql('nvd', conn, if_exists='replace', index = False)
		i += 1
	else:
		sqldf.to_sql('nvd', conn, if_exists='append', index = False)
		i += 1
					

print('Download complete, please check the database.')


