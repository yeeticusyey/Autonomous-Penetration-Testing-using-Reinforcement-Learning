fwimport js2py
#tool to enable javascript running in python
#this tool enables auto translation
import datetime
import wget 
import gzip
import shutil
import sqlite3
import os
import pandas as pd
import json


try:
	conn = sqlite3.connect('nvdtest.db')
	print("Opened database successfully")

except Exception as e:
	print("Error during connection: ", str(e))


i = 2002;
#The oldest NVD database is in 2002

current_date = datetime.date.today()
year = current_date.year

# variable year indicates the current year

while i <= year:
	
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
	
	#connect to database
	df.to_sql('nvdtest', conn, if_exists='replace',)
	
	
		
	i += 1		
	

	
#*** download recent nvd database		
print("NVD database has been updated")
conn.close()		
	
'''
try:
	conn = sqlite3.connect('nvdtest.db')
	print("Opened database successfully")

except Exception as e:
	print("Error during connection: ", str(e))
	
results = conn.execute("SELECT * FROM nvd")

for row in results:
	print (row)
	
conn.close()
'''


#while [ $i - le $year]; do
#	wget https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-$i.json.gz 
#	gunzip nvdcve-1.1-$i.json.gz
#	
#	i = 'expr $i + 1' 




#below is testing codes


js1 = 'console.log("Hello World")'

res1 = js2py.eval_js(js1)
