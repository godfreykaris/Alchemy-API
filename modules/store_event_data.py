import json

class EventDataStore:
    def __init__(self, database_object):
        self.database_object = database_object
    
    def store_event_data(self, contract_address, event_name, transaction_hash, event_data):
        #Get the database connection
        database_connection = self.database_object.get_database_connection()
        
        cursor = database_connection.cursor() 
        
        insert_query = "INSERT INTO contract_" + contract_address + "_events (event_name, transaction_hash, event_data) VALUES (%s, %s, %s); "
        cursor.execute(insert_query, (event_name, transaction_hash, json.dumps(event_data)))

        database_connection.commit()
        cursor.close()
        database_connection.close()
        
    def is_duplicate_event(self, contract_id, event_name, transaction_hash):
        #Get the database connection
        database_connection = self.database_object.get_database_connection()
        
        cursor = database_connection.cursor() 
        
        query = "SELECT EXISTS ( SELECT 1 FROM contract_" + contract_id + "_events WHERE event_name = %s AND transaction_hash = %s);"
        
        cursor.execute(query, (event_name, transaction_hash))
        exists = cursor.fetchone()[0]
        
        cursor.close()
        database_connection.close()
        
        return exists