
class ViewExtracter:
    def get_view(self, web3, contract, function_name):
           
        # Check if the function has inputs/arguments
        function_abi = next((item for item in contract.abi if item["name"] == function_name), None)
                    
        if "inputs" in function_abi:
            inputs = function_abi["inputs"]
            
            if len(inputs) > 0:
                print()
                print(f"Function '{function_name}' requires {len(inputs)} argument(s):")

            user_inputs = []
            for arg in inputs:
                arg_name = arg["name"]
                arg_type = arg["type"]
                
                #Some arguments may not have names
                if(arg_name != ""):
                    print(f"Argument name: {arg_name}, Type: {arg_type}")
                else:
                    print(f"Argument Type: {arg_type}")
                
                # Perform action based on the argument name
                if arg_type == "address":
                    # Input an Ethereum address
                    address_input = input("Enter the address argument value: ")
                    
                    # Validate and format the address
                    address = None
                    if address_input.startswith("0x") and len(address_input) == 42:
                        # Remove the "0x" prefix and convert to lowercase
                        address = address_input[2:].lower()
                        address =  web3.to_checksum_address(address)
                    else:
                        print("Invalid Ethereum address format!")
                        exit()
                    
                    user_inputs.append(address)
                elif arg_type == "uint256":
                    try:
                        # Input an unsigned integer
                        uint_value = input("Enter the uint256 argument value: ")
                        if uint_value < 0:
                            raise ValueError("Invalid uint256 value: Negative numbers not allowed")
                        
                        user_inputs.append(uint_value)
                    except ValueError as e:
                        print("Error:", str(e))
                        exit()

                elif arg_type == "bool":
                    # Input a boolean value
                    boolean_input = input("Enter the boolean argument value (True/False): ")
                    boolean = boolean_input.lower() == "true"

                    user_inputs.append(boolean)

                elif arg_type == "string":
                    # Input a string
                    string = input("Enter the string argument value: ")
                    user_inputs.append(string)
            
            print()
        else:
            print(f"Function '{function_name}' does not have any arguments.")
            print()
             
        try:
            if len(user_inputs) > 0 :
                result = contract.functions[function_name](user_inputs[0]).call()
            else:
                result = contract.functions[function_name]().call()
                
            return result
        except Exception as e:
            print(f"Error retrieving data for function '{function_name}': {str(e)}")
            print()
            return "Error"
    
    def perform_view_function_call(self, web3, contract):    
        # Get the list of view functions (constant functions)
        view_functions = [fn for fn in contract.abi if fn['type'] == 'function' and fn['stateMutability'] == 'view']

        print()
        print("These are the available view functions. Choose One.")
        print()
        # Loop through each view function and get its data
        counter = 1
                
        for function in view_functions:
            print('{}'.format(counter) + ": " + function['name'])
            counter = counter + 1
        
        print()
        # Get user input
        choice = int(input("Enter the number corresponding to the function you choose: "))
        
        if(choice <= 0 or choice > counter):
            print("Invalid choice")
        else:          
            function_name = view_functions[choice - 1]['name']    

            result = self.get_view(web3, contract, function_name)
            
            if(result != "Error"):
                json_data = {}
                json_data["function_name"] = function_name 
                json_data["result"] = result
                
                return json_data
            else:
                json_data = {}
                json_data["Status"] = "An error occurred!"
                json_data["Error"] = "Please ensure you have the correct arguments for the " + function_name + " function."
                
                return json_data
                