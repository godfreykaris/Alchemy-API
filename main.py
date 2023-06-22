from psycopg2 import errors

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from modules.database_initialization import DatabaseInitializer
from modules.web3_iniitialization import Web3Initializer
from modules.contracts_handler import ContractsHandler

from modules.get_event_data import EventDataExtracter
from modules.store_event_data import EventDataStore


#Initialize Web3
web3_initializer = Web3Initializer("https://mainnet.infura.io/v3/c801c82431594bf1935b736f68d13c08")

#Create the contracts handler
contracts_handler = ContractsHandler(web3_initializer.web3)

#Initialize the database
database_initializer = DatabaseInitializer("config.json")

#Prepare to store event logs to the database
event_data_store = EventDataStore(database_object=database_initializer)

while True:
    
    #Get the contracts from the database
    contracts = contracts_handler.get_contracts(database_object=database_initializer)
    
    for contract_data in contracts:
        contract = contracts_handler.initialize_contract(contract_data['contract_address'], contract_data['contract_abi'])
        
        for event in contract.events:   
            #Create the event data extracter
            event_data_extracter = EventDataExtracter(web3_initializer.web3, contract); 
            
            #Get Event logs for the given event
            event_logs = event_data_extracter.get_event_logs(event.__name__)

            if len(event_logs) > 0:
                log = event_logs[-1]                
                
                contract_id = '{}'.format(contract_data['id'])                 
                
                #Create the events table if it does not exist
                contracts_handler.create_contract_events_table(database_object=database_initializer, contract_id=contract_id)
                                
                #Make sure it is not a duplicate
                is_duplicate_event = event_data_store.is_duplicate_event(contract_id, event.__name__, log['transactionHash'].hex())
                if(is_duplicate_event == False):
                    event_data_store.store_event_data(contract_id, event.__name__ , log['transactionHash'].hex(), log)
            
    print()

  




