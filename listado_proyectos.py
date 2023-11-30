import os
import streamlit as st
import pandas as pd
from pathlib import Path
import json
import sqlite3
import uuid
import secrets
import string


def create_project(project_code, project_name, country):
    new_project = pd.DataFrame([[project_code, project_name, country]],
                               columns=['Project Code', 'Project Name', 'Country'])
    new_project.to_csv("listado_proyectos.csv", mode='a', header=False, index=False)

def listado_proyectos():
    file = 'listado_proyectos.csv'
    st.title("Datos Proyectos")

    # Section control
    section = st.radio("", ["Mostrar Listado", "Agregar Proyecto", "Eliminar Proyecto"])

    if section == "Mostrar Listado":
        if os.path.exists(file):
            proyectos = pd.read_csv(file)
            st.markdown(proyectos.to_html(index=False), unsafe_allow_html=True)
        else:
            st.warning("No hay proyectos registrados.")

    elif section == "Agregar Proyecto":
        st.subheader("Agregar Proyecto")
        project_code = st.text_input("Código del Proyecto:")
        project_name = st.text_input("Nombre del Proyecto:")
        country = st.text_input("País:")

        if st.button("Guardar Proyecto"):
            create_project(project_code, project_name, country)
            st.success(f"Se ha agregado el proyecto {project_name}.")

    elif section == "Eliminar Proyecto":
        st.subheader("Eliminar Proyecto")
        if os.path.exists(file):
            proyectos = pd.read_csv(file)
            project_options = ["Seleccionar proyecto..."] + list(proyectos['Project Name'])
            selected_project = st.selectbox("Selecciona un proyecto para eliminar:", project_options)

            if st.button("Eliminar"):
                if selected_project == "Seleccionar proyecto...":
                    st.warning("Por favor, selecciona un proyecto para eliminar.")
                else:
                    proyectos = proyectos[proyectos['Project Name'] != selected_project]
                    proyectos.to_csv(file, index=False)
                    st.success(f"Se ha eliminado el proyecto {selected_project}.")
        else:
            st.warning("No hay proyectos registrados para eliminar.")
