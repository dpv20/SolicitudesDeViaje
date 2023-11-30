import os
import streamlit as st
import pandas as pd
from pathlib import Path
import json
import sqlite3
import uuid
import secrets
import string

def create_email(email_address, email_type):
    new_email = pd.DataFrame([[email_address, email_type]],
                             columns=['mails', 'type'])
    new_email.to_csv("mails.csv", mode='a', header=False, index=False)

def mail_list():
    file = 'mails.csv'
    st.title("mails")

    # Load data
    if not os.path.exists(file) or os.stat(file).st_size == 0:
        mails = pd.DataFrame(columns=['mails', 'type'])
    else:
        mails = pd.read_csv(file)
        if 'mails' not in mails.columns or 'type' not in mails.columns:
            mails = pd.DataFrame(columns=['mails', 'type'])

    # Email action selection
    action = st.radio("Choose an action:", ["Mostrar Listado", "Add Email", "Delete Email"])

    if action == "Mostrar Listado":
        st.markdown(mails.to_html(index=False), unsafe_allow_html=True)

    # Add email section
    elif action == "Add Email":
        st.write("## Add Email")
        new_mail = st.text_input("New Email")
        types = ['Operaciones', 'Arquitectura', 'Ingenieria', 'Otros']
        new_type = st.selectbox('Type', types)
        if st.button("Add Email"):
            if new_mail not in mails['mails'].values:
                create_email(new_mail, new_type)
                st.success(f"Email {new_mail} has been added.")  # Success message for email addition
            else:
                st.error(f"Email {new_mail} is already in the list.")

    # Delete email section
    elif action == "Delete Email":
        st.write("## Delete Email")
        delete_mail = st.text_input("Email to delete")
        if st.button("Delete Email"):
            if delete_mail in mails['mails'].values:
                mails = mails[mails.mails != delete_mail]
                mails.to_csv(file, index=False)
                st.success(f"Email {delete_mail} has been deleted.")  # Success message for email deletion
            else:
                st.error(f"Email {delete_mail} not found.")
