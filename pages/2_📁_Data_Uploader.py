import streamlit as st
from utils.file_procesing import process_file
from sqlalchemy import create_engine, inspect
from sqlalchemy.sql import text

engine = create_engine("sqlite:///./data/storage.db", echo=False)

st.title('📁 Data uploader')

with st.form(key="uploader", clear_on_submit=True):
    uploaded_files = st.file_uploader('Drop here your files to process them', type=['csv', 'xlsx'], accept_multiple_files=True)

    file_submited = st.form_submit_button('Process files')

    if file_submited:
        if uploaded_files:
            index = 0
            for uploaded_file in uploaded_files:
                index = process_file(engine, uploaded_file, index)

clear_tables = st.button("🔄 Reset Database")

show_tables = st.toggle("🔍 View Database Tables and Content")

if clear_tables:
    inspector = inspect(engine)

    for table_name in inspector.get_table_names():
        with engine.connect() as connection:
            query = text(f"DROP TABLE \"{table_name}\"")
            connection.execute(query)

if show_tables:
    inspector = inspect(engine)

    if inspector.get_table_names():
        st.header(f"Database Tables and Content")
        try:
            for table_name in inspector.get_table_names():
                st.subheader(f"Table: {table_name}")
                try:

                    with engine.connect() as connection:
                        # Take 5 last rows from the table
                        query = text(f"SELECT * FROM \"{table_name}\" ORDER BY ROWID DESC LIMIT 5")
                        rows = connection.execute(query).fetchall()

                        if rows:
                            st.table(rows)
                        else:
                            st.info(f"No data found in table {table_name}.")
                except Exception as e:
                    st.error(f"Error retrieving data for table {table_name}: {e}")
        except Exception as e:
            st.error(f"Error inspecting database: {e}")

    else:
        st.info("No tables found in database.")