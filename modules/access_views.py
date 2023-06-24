from datetime import date, timedelta, datetime

class ViewAccessor:
    def __init__(self, database_object):
        self.database_object = database_object
    
    def access_views(self, contract_address, function_name="All"):
        try: 
            # Prompt the user for the number of days back they want to view the records for.
            print()
            days_back = input("How many days back should " + function_name + " records for "+ contract_address +" go?: ")
            
            # Get current date
            current_date = date.today()
            
            # User desired date
            user_desired_date = current_date - timedelta(days=int(days_back))
            
            # Check if the user desired date exists
            database_connection = self.database_object.get_database_connection()        
            cursor = database_connection.cursor()       

            contract_views_table = "contract_" + contract_address + "_views"
            if function_name == "All":
                query = f"SELECT created_at FROM " + contract_views_table + "  WHERE CAST(created_at AS DATE) = DATE %s "
                cursor.execute(query, (user_desired_date,))
            else:
                query = f"SELECT created_at FROM " + contract_views_table + "  WHERE CAST(created_at AS DATE) = DATE %s AND view_name = %s;"
                cursor.execute(query, (user_desired_date, function_name))
            
            desired_date_view = cursor.fetchone()
            
            # If there are views for the date
            if desired_date_view == None:
                print()
                print("The date you specified is not available.")
                print()
            
            # Fetch all the views
            # IF the desired date is beyond the available views' dates, we give all the available views
            time = datetime.now()
            current_time = datetime.time(time)
            current_date_time = datetime.combine(current_date, current_time)
            
            # Get all the event views
            if function_name == "All":
                query = "SELECT * FROM " + contract_views_table + " WHERE (created_at BETWEEN %s AND %s)"
                cursor.execute(query, (user_desired_date, current_date_time))
            else:
                query = "SELECT * FROM " + contract_views_table + " WHERE (created_at BETWEEN %s AND %s) AND view_name = %s"
                cursor.execute(query, (user_desired_date, current_date_time, function_name))
            
            views = cursor.fetchall()
            
            # If there are views for the date
            if len(views) > 0:
                print()
                print("These are the available views.")
                # Display the views
                
                for view in views:
                    self.display_view_data(view_data=view)
                   
                    
            else:
                print()
                print("There are no views available.")
                print()
                
        except Exception as e:
            # Handle the exception/error
            print()
            print("An error occurred:", str(e))
            print()
    
    def display_view_data(self, view_data):
        print()
        print("Function Name: ", view_data[1])
        print("Result:        ", view_data[2]["result"])
        print("Timestamp:     ", view_data[3])        
        print()    