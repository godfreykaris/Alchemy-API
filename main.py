from psycopg2 import errors

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from modules.database_initialization import DatabaseInitializer
from modules.web3_iniitialization import Web3Initializer
from modules.contracts_handler import ContractsHandler

from modules.store_event_data import EventDataStore
from modules.get_view import ViewExtracter

#Initialize Web3
web3_initializer = Web3Initializer("https://mainnet.infura.io/v3/c801c82431594bf1935b736f68d13c08")

#Create the contracts handler
contracts_handler = ContractsHandler(web3_initializer.web3)

#Initialize the database
database_initializer = DatabaseInitializer("config.json")

#Prepare to store event logs to the database
event_data_store = EventDataStore(database_object=database_initializer)

#Prepare the object that facilitates the retieval of a view from the contract
view_getter = ViewExtracter()
  

# Processing the event logs
# event_data_store.process_events(contracts_handler=contracts_handler,database_initializer=database_initializer,web3_initializer=web3_initializer,event_data_store=event_data_store)
    
"""-----------------Working with views---------------------"""
# Get the contracts from the database
contracts = contracts_handler.get_contracts(database_object=database_initializer) 

contract_data = contracts[0]

contract = contracts_handler.initialize_contract(contract_data['contract_address'], contract_data['contract_abi'])

# The user chooses the function they want to call and the result(view) is printed
view_getter.print_chosen_view(contract)

"""--------------------------------------------------------------------------------"""

