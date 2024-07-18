# SqlAlchemy API
This project allows a python client to interact with Optimisis Etherium contracts and a Supabase PostgreSQL database

This is a backend system that uses FastAPI and SQLAlchemy for managing and interacting with Ethereum Smart Contracts.

## Features
Here are the main endpoints for interacting with this backend:

1. **Add new contract:** `base_url/new_contract/{contract_address}/{contract_abi}`
   - This endpoint allows you to insert a new contract record in the contracts table in the database. The contract_abi should be in JSON format.
   - Example: `base_url/new_contract/0xD74D825286961b06986943CA3Bb97D9B6b7aAd92/<contract_abi_in_json_format>`

2. **Listening for events:** `base_url/get_events_logs/`
   - This endpoint allows you to record the events in the database as they happen at realtime.

3. **Print view functions:** `base_url/view_functions_and_inputs/{contract_address}`
   - This endpoint lists the view functions as well as their inputs if they take any. It takes in the contract address.
   - Example: `base_url/view_functions_and_inputs/0xD74D825286961b06986943CA3Bb97D9B6b7aAd92`

4. **Invoke view function:** `base_url/invoke_view_function/{contract_address}/{function_name}/{arguments}`
   - This endpoint allows you to perform view function calls and view the output (view). This output is also recorded in the database. You provide the function name and arguments (inputs) if any.
   - Example without arguments: `base_url/invoke_view_function/0xD74D825286961b06986943CA3Bb97D9B6b7aAd92/winnerNumber?arguments=`
   - Example with arguments: `base_url/invoke_view_function/0xD74D825286961b06986943CA3Bb97D9B6b7aAd92/entries?arguments=0xD74D825286961b06986943CA3Bb97D9B6b7aAd92&arguments=`

5. **Accessing views:** `base_url/access_views/{contract_address}/{days_back}/{function_name}`
   - This endpoint allows one to access views already stored in the database. It takes in the contract address, the number of days the records should go back, and the function name for which you want the records for.
   - Example one: `base_url/access_views/0xD74D825286961b06986943CA3Bb97D9B6b7aAd92/1/All`
   - Example two: `base_url/access_views/0xD74D825286961b06986943CA3Bb97D9B6b7aAd92/1/winnerNumber`

6. **Accessing event logs:** `base_url/access_events/{contract_address}/{days_back}/{event_name}`
   - This endpoint allows you to view the event logs recorded in the database given the contract address, days back, and the event name.
   - Example one: `base_url/access_events/0xD74D825286961b06986943CA3Bb97D9B6b7aAd92/1/All`
   - Example two: `base_url/access_events/0xD74D825286961b06986943CA3Bb97D9B6b7aAd92/1/Initialized`


## Installation
To set up a virtual environment and activate it, run the following commands:

```shell
python -m venv sqlalchemyenv 
source sqlalchemyenv/bin/activate

## Required Packages
You need the following Python packages to interact with the backend:

- `web3`
- `fastapi`
- `attributedict`
- `sqlalchemy`
- `psycopg2-binary`
- `uvicorn`

To install the packages, use the following command:

```shell
pip install web3 fastapi attributedict sqlalchemy psycopg2-binary uvicorn


To run the app, use:
- uvicorn main:app --host 0.0.0.0 --reload

Please note that the above command will install all the listed packages at once.
