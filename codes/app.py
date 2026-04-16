import streamlit as st

from main import fun_rollup


def run_app():
    st.set_page_config(layout="wide", page_title="Account Structure Processing")
    st.title("Database Input Form")

    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = None
    if 'rollup_error' not in st.session_state:
        st.session_state['rollup_error'] = None
    if 'rolled_up_df' not in st.session_state:
        st.session_state['rolled_up_df'] = None

    col_form, col_output = st.columns([1, 1])

    with col_form:
        st.header("Input Form")
        with st.form(key='input_form'):
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                username = st.text_input("Username", value='test')
                password = st.text_input("Password", type='password', value='test123')
                host_name = st.text_input("Host Name", value='192.168.1.70')
                port = st.text_input("Port", value='1521')
                service_name = st.text_input("Service Name", value='orclpdb')

            with col2:
                payer_name = st.selectbox("Payer Name", options=['TX', 'IL','BBA'], index=0)
                account_structure = st.text_input("Account Structure", value='AS-TX.xlsx')
                sheet = st.text_input("Sheet", value='AS')
                as_columns_to_read = st.text_input("AS Columns to Read", value='TX')
                remarks = st.text_input("Remarks", value='rolled_up')

            submit_button = st.form_submit_button(label='Submit')

    with col_output:
        st.header("User Provided Input")
        if submit_button:
            st.session_state['user_input'] = {
                "username": username,
                "password": password,
                "host_name": host_name,
                "port": port,
                "service_name": service_name,
                "payer_name": payer_name,
                "as_columns_to_read": as_columns_to_read,
                "account_structure": account_structure,
                "sheet": sheet,
                "remarks": remarks,
            }

            error, rolled_up_df = fun_rollup(
                username=username,
                password=password,
                host_name=host_name,
                port=port,
                service_name=service_name,
                payername=payer_name,
                as_columns_to_read=as_columns_to_read,
                account_structure=account_structure,
                sheet=sheet,
                remarks=remarks,
            )
            st.session_state['rollup_error'] = error
            st.session_state['rolled_up_df'] = rolled_up_df

        if st.session_state['user_input']:
            st.json(st.session_state['user_input'])
        else:
            st.info("Fill out the form and submit to see input here.")

    st.write("---")
    st.header(f"Rolled-up Output preview for payer {st.session_state['user_input']['payer_name'] if st.session_state['user_input'] else 'N/A'}")

    if st.session_state['rollup_error']:
        st.error(f"Rollup failed: {st.session_state['rollup_error']}")
    elif st.session_state['rolled_up_df'] is not None:
        def highlight_rolled_up(row):
            user_remarks = st.session_state['user_input'].get('remarks', 'rolled_up') if st.session_state['user_input'] else 'rolled_up'
            return ['background-color: yellow' if row['remarks'] == user_remarks else '' for _ in row]
        styled_df = st.session_state['rolled_up_df'].style.apply(highlight_rolled_up, axis=1)
        st.dataframe(styled_df, use_container_width=True, height=800)
    else:
        st.info("Submit the form to generate rolled-up values.")

if __name__ == '__main__':
    run_app()
