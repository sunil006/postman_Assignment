# Postman_Assignment

A. Steps run code

	  docker-compose run web python ./Public_API.py .                           # Add sudo infront if you are using Linux
  
  	If your machine is Linux, you need to install docker-compose using this link : https://docs.docker.com/compose/install/
	Note : Didn't do volume mapping as I don't know your system folder structure.

From Table I am showning top 5 rows.

B. Schema and Tables 

	postman(API,Description,Auth,HTTPS,CORS,Link,Category)
	
	Only One table created for every category

	No need to Recreate them. Creating table from python script, which is present in Public_API.py .

C. Points to achieve

	1. Authorization and Token expiration is done.Created Token if it got expired by using its response code.
	   For Authorization, generating token in the begining of the code and if it gets 10 requests in one minute 
	   it goes to sleep for  65 seconds and then it starts again from the last point.
	2. Pagination is done for each category.
	3. Rate limiting is also done.
	4. OOPS are also included.
	5. Crawled all APIs.
	
	Number of entries in the table depends on the API data they provide by that category.

D. Points that not achieved

	Achieved everything.
