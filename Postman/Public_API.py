import requests
import json
import itertools
from Bearer import BearerAuth
import psycopg2
import pandas as pd
import pandas.io.sql as psql
import time
connection = psycopg2.connect(user='postgres',password='postgres',host='db',port="5432",database='postgres')
cursor = connection.cursor()


class Meta_Info():
	
	@staticmethod
	def Token_Creation(token_url):
		t=requests.get(token_url)
		t=t.text
		t=json.loads(t)
		t=t["token"]
		return t

	@staticmethod
	def Categories(category_url,pages,token_url):
		token=Meta_Info().Token_Creation(token_url)
		Categories=[]
		for i in pages:
			c=requests.get(category_url+i,auth=BearerAuth(token))
			c=c.text
			c=json.loads(c)
			c=c['categories']
			Categories.append(c)

		Categories = list(itertools.chain(*Categories))
		Categories[3] = 'Art %26 Design'
		Categories[7] = 'Cloud Storage %26 File Sharing'
		Categories[14] = 'Documents %26 Productivity'
		Categories[18] = 'Food %26 Drink'
		Categories[19] = 'Games %26 Comics'
		Categories[32] = 'Science %26 Math'
		Categories[36] = 'Sports %26 Fitness'
		Categories = list(itertools.chain(*Categories))
		return Categories

	@staticmethod
	def Generate_Url(base_url,Categories,pages):
		All_Urls=[]
		for c in Categories:
			for p in pages:
				url = base_url+p+'&category='+c
				All_Urls.append(url)

		return All_Urls



class Crawler():

	@staticmethod
	def process_data(response):
		data=response.text
		data=json.loads(data)
		data=data["categories"]
		
		return data
	
	
	@staticmethod
	def crawl(base,token_url,category_url,pages):
		token=Meta_Info().Token_Creation(token_url)
		s=Meta_Info().Categories(category_url,pages,token_url)
		url_list=Meta_Info().Generate_Url(base,s,pages)

		i=0		
		while(i<len(url_list)):
			print(i)
			response = requests.get(url_list[i], auth=BearerAuth(token))
			print(response)
			if (response.status_code==200):
				data=Crawler.process_data(response)
				Crawler.Populate_data(data)
			elif(response.status_code==429):
				print("Limit reached for requests per minute")
				print("Wait for one minute....")				
				time.sleep(65)

				i=i-1
			elif(response.status_code==403):
				print("Token got exipered")				
				token=Meta_Info().Token_Creation('https://public-apis-api.herokuapp.com/api/v1/auth/token')
				print("Another token generated and starting again")
				i=i-1
			i=i+1

	@staticmethod
	def Populate_data(data):


		try:
					
			cursor = connection.cursor()
			postgres_insert_query = """ INSERT INTO postman(API,Description,Auth,HTTPS,CORS,Link,Category) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
			for d in range(0,len(data)):
				
				record_to_insert = (data[d]['API'],data[d]['Description'], data[d]['Auth'],data[d]['HTTPS'],data[d]['Cors'],data[d]['Link'],data[d]['Category'] )
				cursor.execute(postgres_insert_query, record_to_insert)

			connection.commit()
			count = cursor.rowcount
			print (count, "Record inserted successfully into postman table")

		except (Exception, psycopg2.Error) as error :
			if(connection):
				print("Failed to insert record into postman table", error)

		finally:
				   
			if(connection):
				cursor.close()

				print("PostgreSQL connection is closed")

	@staticmethod
	def Create_Table():
		cursor.execute("DROP TABLE IF EXISTS Postman")
		connection.commit()

		table='''CREATE TABLE Postman(API text,Description text,Auth text,HTTPS text,CORS text,Link text,Category text)'''
		cursor.execute(table)
		print("Success ")
		connection.commit()
		
	@staticmethod
	def show_data():
		table    = pd.read_sql('select * from Postman LIMIT 5', connection)
		print(table)
			
	


#As of now considered only 5 pages.
#Crawled Every API
pages=['1','2','3','4','5','6','7','8','9','10']
base='https://public-apis-api.herokuapp.com/api/v1/apis/entry?page='
token_url='https://public-apis-api.herokuapp.com/api/v1/auth/token'
category_url='https://public-apis-api.herokuapp.com/api/v1/apis/categories?page='

Crawler.Create_Table()
Crawler.crawl(base,token_url,category_url,pages)
Crawler.show_data()

