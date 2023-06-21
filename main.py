import json
import psycopg2

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from web3 import Web3

from modules.get_event_data import EventDataExtracter
from modules.store_event_data import EventDataStore
from modules.database_initialization import DatabaseInitializer

#Get Event data from the contract
event_data_extracter = EventDataExtracter("https://mainnet.infura.io/v3/c801c82431594bf1935b736f68d13c08");
event_data_extracter.initialize_contract("0xdAC17F958D2ee523a2206206994597C13D831ec7", "contract_abi.json")

#Get Event logs for the given event
event_logs = event_data_extracter.get_event_logs("Transfer");


#Initialize the database
database_initializer = DatabaseInitializer("config.json")
database_connection = database_initializer.get_database_connection()

#Store the event logs tin the contract_event table
event_data_store = EventDataStore(database_connection=database_connection)
event_data_store.store_event_data(event_logs=event_logs)


