import pandas as pd 
from db import get_oracle_engine
from mappings_for_account_structure import as_dict
from sqlalchemy import text
from mappings_for_rename import rename_column_mapping
from insert_query import insert_dict
from temp_tbl import payer_temp_tbl_query_generator, payer_temp_tbl_query_update



def fun_rollup(schema_name:str, db_name:str, host_name:str, port:str, service_name:str, payername:str, as_columns_to_read, account_structure:str, sheet:str):
    ''' 
    This function is a generic function. Can be used for all payers to roll up account structure.
    '''   
   
    # IMPORT FROM EXCEL
    df = pd.read_excel(account_structure, sheet_name=sheet, dtype=str)

    # Apply a strip function to all string/object columns
    for col in df.select_dtypes(include=['object','string']).columns:
        df[col] = df[col].str.strip()

    # SELECTING ONLY REQUIRED COLUMNS
    df = df[as_columns_to_read]
    df = df.dropna(how='all')
    #print(df.head())

    #CONNECTING THE DATA BASE:
    engine = get_oracle_engine(schema_name, db_name, host_name, port, service_name)


    if isinstance(engine, str):
        print(f"Connection Failed = {engine}")  # Prints error message
    else:
        print("Connection successful!")
        
        #COLUMN SELECTION
        rename_mapping = rename_column_mapping[payername]
        df = df.rename(columns=rename_mapping)
        #print(df.head())

        #PARAMETERS
        params = df.to_dict(orient='records')
        
        #INSERT VALUES
        insert_query = insert_dict[payername]


      
        try:
           with engine.begin() as conn:
               print('Insert Initiated...')
               conn.execute(text(insert_query),params)
               print('Insert completed')

        except Exception as e:
            print(f"INSERT FAIL!{e}")
   

# ACCOUNT STRUCTURE MAPPING

'''
CONNECTION VALUE ASSIGNMENT
'''
schema_name = ''
db_name = ''
host_name = ''
port = ''
service_name = ''

'''
PAYER SPECIFIC VALUE ASSIGNMENT
'''
payer_name=''
table_name = ''
as_columns_to_read = as_dict[payer_name] 
account_structure = ''
sheet = ''


fun_rollup(schema_name, db_name, host_name, port, service_name, payer_name, as_columns_to_read ,account_structure, sheet)  





