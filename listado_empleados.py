import os
import streamlit as st
import pandas as pd
from pathlib import Path
import json
import sqlite3
import uuid
import secrets
import string


def create_employee(nombre_completo, cargo, departamento, pais, email, compania):
    new_employee = pd.DataFrame([[nombre_completo, cargo, departamento, pais, email, compania]],
                                columns=['nombre completo', 'cargo', 'departamento', 'pais', 'email', 'compania'])
    new_employee.to_csv("datos_empleados.csv", mode='a', header=False, index=False)

def listado_empleados():
    file = 'datos_empleados.csv'
    st.title("Datos Empleados")

    # Section control
    section = st.radio("", ["Mostrar Listado", "Agregar Empleado", "Eliminar Empleado"])

    if section == "Mostrar Listado":
        if os.path.exists(file):
            empleados = pd.read_csv(file)
            st.markdown(empleados.to_html(index=False), unsafe_allow_html=True)
        else:
            st.warning("No hay empleados registrados.")

    elif section == "Agregar Empleado":
        st.subheader("Agregar Empleado")
        nombre_completo = st.text_input("Nombre Completo:")
        cargo = st.text_input("Cargo:")
        departamento = st.text_input("Departamento:")
        pais = st.text_input("País:")
        email = st.text_input("Email:")
        compania = st.text_input("Compañía:")

        if st.button("Guardar Empleado"):
            create_employee(nombre_completo, cargo, departamento, pais, email, compania)
            st.success(f"Se ha agregado a {nombre_completo} como empleado.")

    elif section == "Eliminar Empleado":
        st.subheader("Eliminar Empleado")
        if os.path.exists(file):
            empleados = pd.read_csv(file)
            employee_options = ["Seleccionar empleado..."] + list(empleados['nombre completo'])
            selected_employee = st.selectbox("Selecciona un empleado para eliminar:", employee_options)

            if st.button("Eliminar"):
                if selected_employee == "Seleccionar empleado...":
                    st.warning("Por favor, selecciona un empleado para eliminar.")
                else:
                    empleados = empleados[empleados['nombre completo'] != selected_employee]
                    empleados.to_csv(file, index=False)
                    st.success(f"Se ha eliminado a {selected_employee} como empleado.")
        else:
            st.warning("No hay empleados registrados para eliminar.")
