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


def proyectos():
    
    st.title("Proyectos")
    st.write("Select a parameter to search and enter a value:")

    # Read the CSV file
    df_proyectos = pd.read_csv("proyectos.csv")
    ####


    ####

    # Convert the "Date" column to a datetime object
    #df_proyectos["Date"] = pd.to_datetime(df_proyectos["Date"], format="%Y/%m/%d")
    #df_proyectos["Date"] = pd.to_datetime(df_proyectos["Date"], format="%m/%d/%Y")
    #df_proyectos["Date"] = pd.to_datetime(df_proyectos["Date"])
    df_proyectos["Date"] = pd.to_datetime(df_proyectos["Date"]).dt.date

    # Create a list of columns to use in the dropdown
    columns = [
    "Country", "Project Name", "Area", "Region",
    "Type of Lagoon", "XS", "S", "M", "L", "Maximum Lagoon Depth",
    "Total Perimeter", "Wall", "Beach Entrance", "Island beach entrance",
    "Machine Room", "Date", "Estado", "Username", "Decimal Separator"
    ]

    search_columns = [
        "Country", "Project Name", "Region",
        "Machine Room", "Date", "Estado", "Username"
    ]

    display_columns = [col for col in columns if col not in ["Decimal Separator", "TAG"]]
    #display_columns.remove("Area")
    #display_columns.remove("Wall")

    # Create two columns
    col1, col2 = st.columns(2)

    # Create a dropdown to select the parameter in the first column
    parameter = col1.selectbox("Parameter", search_columns)


    if parameter == "Date":
        # If "Date" is selected, display a date input for the date range
        date_range = col2.date_input("Select date range", [datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()], key=parameter)

        if len(date_range) == 2:
            start_date, end_date = date_range[0], date_range[1]

            # Convert the start_date and end_date to datetime64[ns] dtype
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

            # Filter the dataframe based on the selected date range
            filtered_df = df_proyectos[(df_proyectos["Date"] >= start_date) & (df_proyectos["Date"] <= end_date)]
        elif len(date_range) == 1:
            st.warning("Please select both start and end dates.")
            filtered_df = pd.DataFrame()
        else:
            filtered_df = df_proyectos.copy()
    else:
        # Get unique values from the selected column
        unique_values = df_proyectos[parameter].unique()
        # Create a multiselect input field with unique values in the second column
        search_values = col2.multiselect("Search values", unique_values, key=parameter)

        # Filter the dataframe based on the selected parameter and search values
        # If no search values are selected, display the complete dataframe
        if search_values:
            filtered_df = df_proyectos[df_proyectos[parameter].isin(search_values)]
        else:
            filtered_df = df_proyectos.copy()

    # Remove the "Decimal Separator" column from the displayed dataframe


    try:
        filtered_df = filtered_df[display_columns]
    except KeyError:
        st.write('ingrese la segunda fecha')
        # code to run if the above code raised an exception of type ExceptionType


    #space
    st.write('')



    # Display the filtered dataframe
    st.write(filtered_df)
