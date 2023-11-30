import os
import streamlit as st
import pandas as pd
from pathlib import Path
import json
import sqlite3
import uuid
import secrets
import string
from datetime import datetime


def solicitudes_por_usuario(username):
    file = 'solicitudes_viaje.csv'
    st.title("Solicitudes de Viaje por Usuario")

    if username and os.path.exists(file):
        solicitudes = pd.read_csv(file)

        # Filter the data to show only the solicitudes related to the entered username
        solicitudes_usuario = solicitudes[solicitudes['Nombre Empleado'] == username]

        if solicitudes_usuario.empty:
            st.warning("No hay solicitudes para el usuario especificado.")
        else:
            st.markdown(solicitudes_usuario.to_html(index=False), unsafe_allow_html=True)
    elif not username:
        st.warning("Por favor, ingrese un nombre de usuario.")
    else:
        st.warning("No hay solicitudes registradas.")
