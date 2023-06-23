
import json

from psycopg2.extras import RealDictCursor

class ContractsHandler:
    def __init__(self, web3):        
        self.web3 = web3            
               
    def initialize_contract(self, contract_address, contract_abi):
        # Get the contract abi
        abi = json.dumps(contract_abi) 
            
        # Instantiate the contract
        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        
        return contract
        
    def get_contracts(self, database_object):
        #Get the database connection
        database_connection = database_object.get_database_connection()
        
        cursor = database_connection.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM contracts"
        cursor.execute(query)

        contracts = cursor.fetchall()
        
        cursor.close()
        database_connection.close()
        
        return contracts

    def create_contract_events_table(self, database_object, contract_address):
        #Get the database connection
        database_connection = database_object.get_database_connection()
        
        cursor = database_connection.cursor(cursor_factory=RealDictCursor)
        query = "CREATE TABLE IF NOT EXISTS contract_" + contract_address + "_events ( id SERIAL PRIMARY KEY, event_name VARCHAR(255) NOT NULL, transaction_hash VARCHAR(255) NOT NULL,    event_data JSON,    timestamp TIMESTAMP DEFAULT NOW());"
        cursor.execute(query)

        database_connection.commit()
        
        cursor.close()
        database_connection.close()

    
    