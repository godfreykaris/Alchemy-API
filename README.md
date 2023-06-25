**Project Setup**<br/>
Database Installation
  1.	Setup a local PostgreSQL database.
  2.	Here is a step by step guide: https://www.prisma.io/dataguide/postgresql/setting-up-a-local-postgresql-database
  3.	Look for pgAdmin and launch it.
  4.	pgAdmin location:<br/>
      -	Linux: On Linux pgAdmin is available under Programming in the Applications menu
      -	Mac: On a Mac it is available in the Applications folder as an application
      -	Windows: On Windows it is available under Program Files

Create a database
  1.	In pgAdmin, right-click the Databases node and select Create > Database… menu item
  2.	It will show a dialog for you to enter detailed information on the new database.
  3.	Enter the name of the database and select an owner in the general tab.
  4.	Click the SQL tab to view the generated SQL statement that will execute.
  5.	Finally, click the Save button to create the database. You will see the database listed on the database list

Create the contracts table:
  1.	Go to "tables" in pgAdmin window in the database you created, right click on "tables" and click on "New Table".
  2.	This will open a new window to create a New Table. Supply “contracts” as the name of your new table and then click on Columns
  3.	Now in the columns window, add the following columns using the given data types:<br/>
      -	id: integer notNull Primary Key
      -	contract_address: VARCHAR 255
      -	contract_abi: json
Add the test contract:
  1.	Right-click on your table –> select View/Edit Data –> All Rows
  2.	Add new row 
      Use the 0xdAC17F958D2ee523a2206206994597C13D831ec7 as the contract address and the contents of the contract_abi. json file in the main directory.
  3.	Click on the 'Save' button on the menu bar near the top of the data window.


Cloning the repository
  1.	Clone the repository to your local machine.
  2.	Install Python
  3.	Install the following packages using pip:
    -	web3
    -	pyscopg2
    -	sqlalcemy
    -	json
    -	fastapi
    -	json
    -	attributeddict



**Program Files**<br/>
The modules folder contains the following key files:
1.	web3_initialization.py – this file contains a constructor that takes an endpoint that is used to interact with the contract via web3.

2.	database_initialization.py – this file contains the functions to get the database credentials from the config.json file and also to get a database connection.

3.	contracts_handler.py – it contains functions to initialize contracts, retrieving all contracts from the contracts table as well as creating the events and views table dynamically.

4.	get_event_data.py – this file contains a class with a constructor that takes in a web3 object as well as a contract object. It also contains the methods used to extract the contract logs from a contract given an event name.  Below is the output during the process of getting events:
![Get events  expected Output](https://github.com/KotlinMaestro/Alchemy-API/blob/contracts/contracts-processing/output_during_event_recording.png)

5.	store_event_data.py – this file handles the storage of the event data extracted from the contract to the database in a contract event table with the following name format contract_<contract address>_events. If the required table does not exist, it is created dynamically. Below is how the events are stored in the database:
![Stored Events](https://github.com/KotlinMaestro/Alchemy-API/blob/contracts/contracts-processing/event_logs_image.png)

6.	access_events.py – this file handles the retrieval of event log from the database as well as displaying them. The access_events function can take or not take the event name. If it is not provided with the event name, it  retrieves all the logs upto the number of days the user has chosen to go back. Otherwise, it retrieves for the given event name. Below is an image showing the result of accessing all events:
![Accessing  events Output](https://github.com/KotlinMaestro/Alchemy-API/blob/contracts/contracts-processing/accessing_event_logs.png)

7.	get_view.py – this file contains functions to invoke view functions, and getting the output/view. The get_view function also prompts  the user for arguments if the function requires inputs. Below is an image showing the process of invoking a view function:
![Get views  expected Output](https://github.com/KotlinMaestro/Alchemy-API/blob/contracts/contracts-processing/performing_a_view_call.png)

8.	store_view.py – this file is responsible for storing the view function call result in the database. Below is how the views are stored in the database:
	![Stored Views](https://github.com/KotlinMaestro/Alchemy-API/blob/contracts/contracts-processing/views_image.png)

9.	Access_views.py – this file, as the get_events file, retrieves the stored views from the contract_<contract address>_views and displays the result. Below is an image showing the result of accessing all the views:
![Access views  expected Output](https://github.com/KotlinMaestro/Alchemy-API/blob/contracts/contracts-processing/accessing_views.png)

10.	main.py – the main function contains the function calls. You can uncomment them in the order they are given one by one while testing.

