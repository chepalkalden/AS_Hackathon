import pandas as pd
from db import get_oracle_engine
from As import as_dict
from sqlalchemy import text
from rename import rename_column_mapping
from insert_query import insert_dict
from typing import Sequence, Mapping, Any, cast, Optional, Tuple


def normalize_columns(as_columns_to_read):
    if isinstance(as_columns_to_read, list):
        return as_columns_to_read
    as_columns_to_read = str(as_columns_to_read).strip()
    if not as_columns_to_read:
        return []
    if as_columns_to_read in as_dict:
        return as_dict[as_columns_to_read]
    if ',' in as_columns_to_read:
        return [col.strip() for col in as_columns_to_read.split(',') if col.strip()]
    return [as_columns_to_read]


def fun_rollup(username: str, password: str, host_name: str, port: str, service_name: str, payername: str, as_columns_to_read, account_structure: str, sheet: str, remarks: str) -> Tuple[Optional[str], Optional[pd.DataFrame]]:
    '''
    This function is a generic function. Can be used for all payers to roll up account structure.
    '''

    df = pd.read_excel(account_structure, sheet_name=sheet, dtype=str)
    for col in df.select_dtypes(include=['object', 'string']).columns:
        df[col] = df[col].str.strip()

    columns = normalize_columns(as_columns_to_read)
    if not columns:
        return 'No columns were provided to read from the Excel file.', None

    df = df[columns]
    df = df.dropna(how='all')

    engine = get_oracle_engine(username, password, host_name, port, service_name)
    if isinstance(engine, str):
        return f'Connection Failed = {engine}', None

    rename_mapping = rename_column_mapping.get(payername)
    if rename_mapping is None:
        return f'Unknown payer name: {payername}', None

    df = df.rename(columns=rename_mapping)

    def infer_statusname(row):
        status = str(row.get('statusname', '') or '').strip()
        if status:
            return status

        for field in ('badescription', 'categorydescription'):
            text_value = str(row.get(field, '') or '').upper()
            if 'ACTIVE' in text_value:
                return 'ACTIVE'
            if 'COBRA' in text_value:
                return 'COBRA'

        return status

    df['statusname'] = df.apply(infer_statusname, axis=1)
    df['remarks'] = remarks
    params = df.to_dict(orient='records')
    inserted_df = df.copy()

    insert_query = insert_dict.get(payername)
    if insert_query is None:
        return f'No insert query configured for payer {payername}', None

    try:
        with engine.begin() as conn:
            conn.execute(text(insert_query), cast(Sequence[Mapping[str, Any]], params))
        # After insert, query all records from the table
        table_name = f"HR_{payername}"
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {table_name}"))
            full_df = pd.DataFrame(result.fetchall(), columns=result.keys())
        return None, full_df
    except Exception as e:
        return str(e), None

'''
if __name__ == '__main__':
    #payer_name = 'TX'
    #as_columns_to_read = as_dict[payer_name]
    #account_structure = r'd:\\HACKATHON\\AS_Hackathon\\codes\\AS-TX.xlsx'
    #sheet = 'AS'
    result = fun_rollup(
        username='test',
        password='test123',
        host_name='192.168.1.70',
        port='1521',
        service_name='orclpdb',
        payername=payer_name,
        as_columns_to_read=as_columns_to_read,
        account_structure=account_structure,
        sheet=sheet,
    )
    if result:
        print(f'Error: {result}')
    else:
        print('Rollup completed successfully.')
'''