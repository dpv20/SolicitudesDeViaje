import os
import streamlit as st
import pandas as pd
from pathlib import Path
import json
import sqlite3
import uuid

from streamlit_lottie import st_lottie
from streamlit_extras.switch_page_button import switch_page
from streamlit.source_util import _on_pages_changed, get_pages
import streamlit.components.v1 as components

import shutil

def delete_directory(dir_path):
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        try:
            shutil.rmtree(dir_path)
            print(f"Successfully deleted {dir_path}")
        except Exception as e:
            print(f"Failed to delete {dir_path}. Reason: {e}")

st.set_page_config(page_title="Multipage App", page_icon=":key:")

from functions_webpage import *
from homepage import *
from surveys import *
from stages import *
from proyectos import *
from proyectos_pendientes2 import *  
from user_projects import *
from visitas import *
from send_mail2 import *
from mail_list import *
from solicitud_viaje import *
from listado_empleados import *
from listado_proyectos import *
from listado_viaticos import *
from solicitudes_pendientes import *
from solicitudes_aprobadas import *
from make_checklist import *
from solicitudes_por_usuario import *
from solicitudes_de_area import *

#######################################################
from extras.simcards import *

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'username' not in st.session_state:
    st.session_state['username'] = ""

if 'user_role' not in st.session_state:
    st.session_state['user_role'] = ""

if 'user_position' not in st.session_state:
    st.session_state['user_position'] = ""

if 'area' not in st.session_state:
    st.session_state['area'] = ""


DEFAULT_PAGE = "Login.py"
st.write('-----')

clear_all_but_first_page()

users = load_users("users.csv")
users_df = pd.read_csv("users.csv")
df_empleados = pd.read_csv('datos_empleados.csv')
def main():
    st.markdown(
        """
        <style>
            div[data-testid='stRadio'] div[class^='Widget'] label {
                font-size: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state['logged_in']:
        delete_directory(r'C:\Users\dpv_2\AppData\Local\Temp\gen_py')
        st.sidebar.title('Menu')

        user_position = None
        if st.session_state['username'] in users_df['username'].values:
            user_position = users_df[users_df['username'] == st.session_state['username']]['position'].iloc[0]
            user_area = users_df[users_df['username'] == st.session_state['username']]['area'].iloc[0]


        if st.session_state['user_role'] == 'admin':
            menu_options = ["homepage", "Solicitud de Viaje", "configuraciones"]
        elif user_position == 'director':
            menu_options = ["homepage", "Solicitud de Viaje", "Solicitudes Area"]
        elif user_area == 'Secretary':
            menu_options = ["homepage", "Solicitud de Viaje", "configuraciones"]
        else:
            menu_options = ["homepage", "Solicitud de Viaje"]
        if st.session_state['username'] == 'tmora@crystal-lagoons.com' or st.session_state['username'] == 'dpavez@crystal-lagoons.com':
            menu_options.append("SIM CARDS")

        choice = st.sidebar.selectbox("Menu", menu_options)

        if choice == "homepage":
            homepage()
        elif choice == "Solicitud de Viaje":
            if st.session_state['user_role'] == 'admin':
                viaje_options = [
                    'Crear Solicitud de Viaje',
                    'Solicitudes Pendientes',
                    'Listado Solicitudes Aprobadas',
                    'Listado de Empleados',
                    'Listado de Proyectos',
                    'Listado de Viáticos',
                    'Ver Mis Solicitudes'
                ]
                #holiwi
                viaje_choice = st.sidebar.radio("Opciones de Viaje", viaje_options)

                if viaje_choice == 'Crear Solicitud de Viaje':
                    solicitud(st.session_state['username'],user_area)
                elif viaje_choice == 'Solicitudes Pendientes':
                    solicitudes_pendientes()
                elif viaje_choice == 'Listado Solicitudes Aprobadas':
                    solicitudes_aprobadas()
                elif viaje_choice == 'Listado de Empleados':
                    listado_empleados()
                elif viaje_choice == 'Listado de Proyectos':
                    listado_proyectos()
                elif viaje_choice == 'Listado de Viáticos':
                    listado_viaticos()
                elif viaje_choice == 'Ver Mis Solicitudes':
                    # Obtener el valor del campo 'email' que coincide con st.session_state['username']
                    filtro = df_empleados['email'] == st.session_state['username']
                    Nombre = df_empleados.loc[filtro, 'nombre completo'].iloc[0]  # Asumiendo que solo hay una coincidencia
                    solicitudes_por_usuario(Nombre)
                    #print(Nombre)
            elif user_area == 'Secretary':
                viaje_options = [
                    'Listado Solicitudes Aprobadas',
                    'Crear Solicitud de Viaje',
                    'Listado de Empleados',
                    'Listado de Proyectos',
                    'Listado de Viáticos',
                    'Solicitudes Pendientes',
                    'Ver Mis Solicitudes'
                ]
                viaje_choice = st.sidebar.radio("Opciones de Viaje", viaje_options)
                if viaje_choice == 'Crear Solicitud de Viaje':
                    solicitud(st.session_state['username'], user_area)
                elif viaje_choice == 'Listado Solicitudes Aprobadas':
                    solicitudes_aprobadas()
                elif viaje_choice == 'Listado de Empleados':
                    listado_empleados()
                elif viaje_choice == 'Listado de Proyectos':
                    listado_proyectos()
                elif viaje_choice == 'Listado de Viáticos':
                    listado_viaticos()
                elif viaje_choice == 'Solicitudes Pendientes':
                    solicitudes_pendientes()
                elif viaje_choice == 'Ver Mis Solicitudes':
                    filtro = df_empleados['email'] == st.session_state['username']
                    Nombre = df_empleados.loc[filtro, 'nombre completo'].iloc[0]  # Asumiendo que solo hay una coincidencia
                    solicitudes_por_usuario(Nombre)
            else:
                viaje_options = [
                    'Crear Solicitud de Viaje',
                    'Ver Mis Solicitudes'
                ]
                viaje_choice = st.sidebar.radio("Opciones de Viaje", viaje_options)

                if viaje_choice == 'Crear Solicitud de Viaje':
                    solicitud(st.session_state['username'], user_area)
                elif viaje_choice == 'Ver Mis Solicitudes':
                    # Obtener el valor del campo 'email' que coincide con st.session_state['username']
                    filtro = df_empleados['email'] == st.session_state['username']
                    Nombre = df_empleados.loc[filtro, 'nombre completo'].iloc[0]  # Asumiendo que solo hay una coincidencia
                    solicitudes_por_usuario(Nombre)
                    #print(Nombre)
                    

        elif choice == "configuraciones" and st.session_state['user_role'] == 'admin':
            admin_choice = st.sidebar.radio('Choose an option', ['Crear nuevo usuario', 'listado de usuarios', 'listado de mails'])
            if admin_choice == 'Crear nuevo usuario':
                nuevo_usuario()
            elif admin_choice == 'listado de usuarios':
                display_users(users, 'users.csv')
            elif admin_choice == 'listado de mails':
                mail_list()
        elif choice == "Solicitudes Area":
            # Check if the username matches
            if st.session_state['username'] == 'agonzalez@crystal-lagoons.com':
                # Add radio buttons to the sidebar
                user_position = st.sidebar.radio(
                    "Departamento",
                    ["Operaciones", "Ingeniería"]
                )

                # Update st.session_state based on the selection
                if user_position == "Operaciones":
                    st.session_state['user_position'] = "Technical"
                    st.session_state['area'] = "Technical"
                elif user_position == "Ingeniería":
                    st.session_state['user_position'] = "Engineering"
                    st.session_state['area'] = "Engineering"

            solicitudes_de_area(st.session_state['username'])
        elif choice == "SIM CARDS":
            choice = st.sidebar.radio("Choose an option", ("Enviar mensaje", "Listado de SIM"))
            if choice == "Enviar mensaje":
                simcards()
            elif choice == "Listado de SIM":
                newsimcard()

    
    else:
        login_page()

if __name__ == "__main__":
    main()
