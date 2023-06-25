from psycopg2 import errors

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from modules.database_initialization import DatabaseInitializer
from modules.web3_iniitialization import Web3Initializer
from modules.contracts_handler import ContractsHandler

from modules.store_event_data import EventDataStore

from modules.store_view import ViewDataStore
from modules.get_view import ViewExtracter

from modules.access_events import EventsAccessor
from modules.access_views import ViewAccessor

app = FastAPI()

templates = Jinja2Templates(directory="templates")

#Initialize Web3
web3_initializer = Web3Initializer("https://mainnet.infura.io/v3/c801c82431594bf1935b736f68d13c08")

#Create the contracts handler
contracts_handler = ContractsHandler(web3_initializer.web3)

#Initialize the database
database_initializer = DatabaseInitializer("config.json")

#Prepare to store event logs to the database
event_data_store = EventDataStore(database_object=database_initializer)

#Prepare to store views
view_data_store = ViewDataStore(database_object=database_initializer)

#Prepare the object that facilitates the retieval of a view from the contract
view_getter = ViewExtracter()
  
#Prepare to access the event logs
events_accessor = EventsAccessor(database_object=database_initializer)

#Prepare to access the views
views_accessor = ViewAccessor(database_object=database_initializer)

# Get the contracts from the database
contracts = contracts_handler.get_contracts(database_object=database_initializer) 
contract_data = contracts[0] # We use the first contract for testing

# Processing the event logs
# event_data_store.process_events(contracts_handler=contracts_handler,database_initializer=database_initializer,web3_initializer=web3_initializer)
    
# The user chooses the function they want to call and the result(view) is printed
# view_data_store.process_view(contract_data, contracts_handler, database_initializer, web3_initializer, view_getter)


# Access the event logs
# All logs
#events_accessor.access_events(contract_address=contract_data['contract_address'])

# Only logs for Transfer event
#events_accessor.access_events(contract_address=contract_data['contract_address'], event_name="Transfer")

# Access the views
# All views
@app.get("/", response_class=HTMLResponse)
def access_view_endpoint(request: Request):
    views = views_accessor.access_views(contract_address="0xdAC17F958D2ee523a2206206994597C13D831ec7")
    context = {"request": request, "views": views}
    return templates.TemplateResponse("index.html", context)
    

# Only views for name view function
#views_accessor.access_views(contract_address=contract_data['contract_address'], function_name="name")
