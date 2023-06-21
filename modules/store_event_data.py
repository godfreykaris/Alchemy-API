import json
import psycopg2

class EventDataStore:
    def __init__(self, database_connection):
        self.database_connection = database_connection
    
    def store_event_data(self, event_logs):
        with self.connection.cursor() as cursor:
            for log in event_logs:
                event_name = log.event
                event_data = json.dumps(log.args)

                insert_query = """
                INSERT INTO contract_events (event_name, event_data)
                VALUES (%s, %s);
                """
                cursor.execute(insert_query, (event_name, event_data))

        self.database_connection.commit()