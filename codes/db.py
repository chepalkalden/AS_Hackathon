from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

'''
schema_name = 'SYSTEM'
db_name = 'oracle'        
host_name = '192.168.1.70'
port = '1521'
service_name = 'orcl'    
password = 'DrinkApple@98'
'''

def get_oracle_engine(username: str, password: str, host_name: str, port: str, service_name: str):
    try:
        connection_string = f'oracle+oracledb://{username}:{password}@{host_name}:{port}/?service_name={service_name}'
        engine = create_engine(connection_string)
        print("Oracle engine created successfully.")
        return engine
    except SQLAlchemyError as e:
        print(f"Error occurred while creating Oracle engine: {e}")
        return str(e)
    

 # Replace with the actual password

#get_oracle_engine()