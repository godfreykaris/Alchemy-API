
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
        
    def create_contract_data_table(self, database_object, contract_address, data_type):
        #Get the database connection
        database_connection = database_object.get_database_connection()
        
        cursor = database_connection.cursor(cursor_factory=RealDictCursor)
        
        if(data_type == "Events"):
            query = "CREATE TABLE IF NOT EXISTS contract_" + contract_address + "_events ( id SERIAL PRIMARY KEY, event_name VARCHAR(255) NOT NULL, transaction_hash VARCHAR(255) NOT NULL,    event_data JSON,    recorded_at TIMESTAMP DEFAULT NOW());"
        elif(data_type == "Views"):
            query = "CREATE TABLE IF NOT EXISTS contract_" + contract_address + "_views ( id SERIAL PRIMARY KEY, view_name VARCHAR(255) NOT NULL, view_data JSONB,    created_at TIMESTAMP DEFAULT NOW());"
        else:
            return
        
        cursor.execute(query)

        database_connection.commit()
        
        cursor.close()
        database_connection.close()

    
    