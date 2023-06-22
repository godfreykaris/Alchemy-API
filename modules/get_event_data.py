
class EventDataExtracter:
    def __init__(self, web3, contract):
        self.web3 = web3
        self.contract = contract
        
    
    def get_event_logs(self, event_name):
        # Get the event logs for the given event name
        event_signature = self.web3.keccak(text= event_name + "(uint256)").hex()  # Replace with your event name and parameter type

        event_logs = self.contract.events[event_name]().get_logs(
            {
                "fromBlock": "latest",
                "topics": [event_signature]
            }
        )
        
        return event_logs
        