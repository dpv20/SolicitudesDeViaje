
import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import shutil
from typing import List
import datetime
import os
import win32com.client as win32
import pythoncom
from PyPDF2 import PdfWriter, PdfReader, PdfMerger
from functions_webpage import *
import datetime
import secrets
import string


import os
from pdf2image import convert_from_path
from shutil import copyfileobj
import base64
from io import BytesIO
import streamlit.components.v1 as components


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def get_csv_download_link(file_path, file_name):
    with open(file_path, 'rb') as f:
        bytes_data = f.read()
        b64 = base64.b64encode(bytes_data).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">Download CSV File</a>'
        return href


def Mis_proyectos(username):
    st.title(f"{username}'s Projects")
    df_proyectos = pd.read_csv("proyectos.csv")

    # Filter the data to show only the projects with the specified user
    user_projects = df_proyectos[df_proyectos["Username"] == username]
    temp_file_path = "temp_user_projects.csv"
    user_projects.to_csv(temp_file_path, index=False)
    st.markdown(get_csv_download_link(temp_file_path, "user_projects.csv"), unsafe_allow_html=True)
    os.remove(temp_file_path)
    selected_columns = ["Project Name", "Country", "Date", "Estado", "Username"]
    header_columns = st.columns([3, 2, 2, 2, 3, 2])  # Adjust column widths here
    
    for col, field_name in zip(header_columns, selected_columns):
        col.write(field_name)

    header_columns[-1].write("Action")

    selected_tag = None

    for _, row in user_projects.iterrows():
        row_columns = st.columns([3, 2, 2, 2, 3, 2])  # Adjust column widths here

        for col, field_name in zip(row_columns, selected_columns):
            col.write(row[field_name])

        button_phold = row_columns[-1].empty()
        select_button = button_phold.button("Select", key=row["TAG"])
        if select_button:
            selected_tag = row["TAG"]

        st.write("---")  # Add a horizontal line between rows

    if selected_tag:
        selected_project = user_projects[user_projects["TAG"] == selected_tag].iloc[0]
        if selected_project["Estado"] == "aprobado":
            pdf_path = os.path.join("TEXs", selected_tag, f"{selected_tag}.pdf")
            if os.path.exists(pdf_path):
                images = convert_from_path(pdf_path)
                for image in images:
                    st.image(image, width=1000)
            else:
                st.error("Error displaying the PDF.")
        else:
            st.warning("The selected project is not approved.")
