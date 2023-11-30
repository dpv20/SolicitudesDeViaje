

import streamlit as st
import pandas as pd
from datetime import datetime
import os


def field_visit_form():
    st.subheader("Field Visit Form")
    
    # Read the CSV file
    projects_df = pd.read_csv('proyectos_visitas.csv')
    
    # Get the unique users from the DataFrame
    users = projects_df['name'].unique()
    
    # Create a dropdown to select a user
    selected_user = st.selectbox("Select User", users)
    
    # Display the projects for the selected user
    user_projects = projects_df[projects_df['name'] == selected_user].dropna(axis=1)
    st.write(f"Projects for {selected_user}:")
    st.write(user_projects.drop(columns=['name']).T)  # Remove the 'name' column and transpose the table
    
    # Create a dynamic form with the option to add and remove date ranges
    if 'date_ranges' not in st.session_state:
        st.session_state['date_ranges'] = []

    st.markdown("Date Ranges:")

    for i, date_range in enumerate(st.session_state['date_ranges']):
        start_date, end_date = date_range
        st.markdown(f"Date Range {i + 1}:")
        st.session_state['date_ranges'][i] = (
            st.date_input(f"Visit Beginning {i + 1}", start_date),
            st.date_input(f"Visit End {i + 1}", end_date)
        )

    if st.button("Add Date Range"):
        st.session_state['date_ranges'].append((datetime.today(), datetime.today()))

    if st.button("Remove Date Range") and len(st.session_state['date_ranges']) > 0:
        st.session_state['date_ranges'].pop()

    # Save the data to the CSV file
    if st.button("Submit"):
        new_data = {
            'name': selected_user,
            'date_ranges': st.session_state['date_ranges']
        }
        
        updated_projects_df = projects_df.append(new_data, ignore_index=True)
        updated_projects_df.to_csv('proyectos_visitas.csv', index=False)
        
        st.success("Data saved successfully.")