from web3 import Web3

class EventDataExtracter:
    #The OVM endpoint allows us to interact with the contract via web3
    def __init__(self, ovm_endpoint):
        # Connect to the Optimism OVM endpoint
        self.web3 = Web3(Web3.HTTPProvider(ovm_endpoint))
    
    def initialize_contract(self, contract_address, contract_abi_file):
        # Get the contract abi
        with open(contract_abi_file, 'r') as file:
            contract_abi = file.read() 
            
        # Instantiate the contract
        self.contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)
    
    def get_event_logs(self, event_name):
        # Get the event logs for the given event name
        event_signature = self.web3.keccak(text= event_name + "(uint256)").hex()  # Replace with your event name and parameter type

        event_logs = self.contract.events[event_name]().get_logs(
            {
                "fromBlock": 0,
                "toBlock": "latest",
                "topics": [event_signature]
            }
        )
        
        return event_logs
        