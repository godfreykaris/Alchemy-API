
from datetime import date, timedelta, datetime

class EventsAccessor:
    def __init__(self, database_object):
        self.database_object = database_object
    
    def access_events(self, contract_address, event_name="All"):
        
        try: 
            # Prompt the user for the number of days back they want to view the logs for.
            print()
            days_back = input("How many days back should the logs for "+ contract_address +" go?: ")
            
            # Get current date
            current_date = date.today()
            
            # User desired date
            user_desired_date = current_date - timedelta(days=int(days_back))
            
            # Check if the user desired date exists
            database_connection = self.database_object.get_database_connection()        
            cursor = database_connection.cursor()       

            contract_logs_table = "contract_" + contract_address + "_events"
            if event_name == "All":
                query = f"SELECT recorded_at FROM " + contract_logs_table + "  WHERE CAST(recorded_at AS DATE) = DATE %s "
                cursor.execute(query, (user_desired_date,))
            else:
                query = f"SELECT recorded_at FROM " + contract_logs_table + "  WHERE CAST(recorded_at AS DATE) = DATE %s AND event_name = %s;"
                cursor.execute(query, (user_desired_date, event_name))
            
            desired_date_log = cursor.fetchone()
            
            # If there are logs for the date
            if desired_date_log == None:
                print()
                print("The date you specified is not available.")
                print()
            
            # Fetch all the logs
            # IF the desired date is beyond the available logs' dates, we give all the available logs
            time = datetime.now()
            current_time = datetime.time(time)
            current_date_time = datetime.combine(current_date, current_time)
            
            # Get all the event logs
            if event_name == "All":
                query = "SELECT * FROM " + contract_logs_table + " WHERE (recorded_at BETWEEN %s AND %s)"
                cursor.execute(query, (user_desired_date, current_date_time))
            else:
                query = "SELECT * FROM " + contract_logs_table + " WHERE (recorded_at BETWEEN %s AND %s) AND event_name = %s"
                cursor.execute(query, (user_desired_date, current_date_time, event_name))
            
            event_logs = cursor.fetchall()
            
            # If there are logs for the date
            if len(event_logs) > 0:
                print()
                print("These are the available logs.")
                # Display the logs
                for event_log in event_logs:
                    event_log_data = event_log[3] #The data is in the third item of the log
                    self.display_event_log_data(event_log_data=event_log_data)
                    
            else:
                print()
                print("There are no logs available.")
                print()
                
        except Exception as e:
            # Handle the exception/error
            print()
            print("An error occurred:", str(e))
            print()
    
    def display_event_log_data(self, event_log_data):
        print()
        print("Event:           ", event_log_data["event"])
        print("logIndex:        ", event_log_data["logIndex"])
        print("transactionIndex:", event_log_data["transactionIndex"])
        print("transactionHash: ", event_log_data["transactionHash"])
        print("address:         ", event_log_data["address"])
        print("blockNumber:     ", event_log_data["blockNumber"])
        print("blockHash:       ", event_log_data["blockHash"])
        print("args:            ", event_log_data["args"])
        print()