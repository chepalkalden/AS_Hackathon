import streamlit as st

st.set_page_config(layout="wide")

st.title("Database Input Form")

# Wider columns: 1:1 ratio, but you can adjust, e.g., [2,2] for even more width
col_form, col_output = st.columns([2, 2])

with col_form:
    st.header("Input Form")
    with st.form(key='input_form'):
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            schema_name = st.text_input("Schema Name", value='SCHEMA1')
            host_name = st.text_input("Host Name", value='EAGLE')
            payer_name = st.text_input("Payer Name", value='PAYER1')
            as_columns_to_read = st.text_input("AS Columns to Read", value='PAYER1')

        with col2:
            db_name = st.selectbox("Database Name", options=['oracle', 'mysql', 'postgresql'], index=0)
            port = st.text_input("Port", value='123')
            table_name = st.text_input("Table Name", value='TABLE1')
            account_structure = st.text_input("Account Structure", value='AS1')

        with col3:
            service_name = st.text_input("Service Name", value='SERVICE1')
            sheet = st.text_input("Sheet", value='Account Structure')

        submit_button = st.form_submit_button(label='Submit')

with col_output:
    st.header("User Provided Input")
    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = None

    if submit_button:
        st.session_state['user_input'] = {
            "schema_name": schema_name,
            "db_name": db_name,
            "host_name": host_name,
            "port": port,
            "service_name": service_name,
            "payer_name": payer_name,
            "table_name": table_name,
            "as_columns_to_read": as_columns_to_read,
            "account_structure": account_structure,
            "sheet": sheet
        }

    if st.session_state['user_input']:
        st.json(st.session_state['user_input'])
    else:
        st.info("Fill out the form and submit to see output here.")
