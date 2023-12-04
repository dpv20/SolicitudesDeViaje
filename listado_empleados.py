import os
import streamlit as st
import pandas as pd

def create_employee(nombre_completo, cargo, departamento, pais, email, compania):
    new_employee = pd.DataFrame([[nombre_completo, cargo, departamento, pais, email, compania]],
                                columns=['nombre completo', 'cargo', 'departamento', 'pais', 'email', 'compania'])
    new_employee.to_csv("datos_empleados.csv", mode='a', header=False, index=False)

def listado_empleados():
    file = 'datos_empleados.csv'
    st.title("Datos Empleados")

    # Section control
    #section = st.radio("", ["Mostrar Listado", "Agregar Empleado", "Eliminar Empleado"])
    section = st.radio("Control de Sección", ["Mostrar Listado", "Agregar Empleado", "Eliminar Empleado"], label_visibility='collapsed')

    if section == "Mostrar Listado":
        if os.path.exists(file):
            empleados = pd.read_csv(file)

            # Dropdown for choosing the column to sort by
            sort_options = empleados.columns.to_list()
            #selected_column = st.selectbox("Selecciona la columna para ordenar:", sort_options)
            selected_column = st.selectbox("Selecciona la columna para ordenar:", sort_options, label_visibility='collapsed')

            # Add Ordenar button
            if st.button("Ordenar", key="ordenar_button"):
                empleados.sort_values(by=selected_column, inplace=True)
                empleados.to_csv(file, index=False)
                st.success(f"Lista ordenada por {selected_column}.")

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

        if st.button("Guardar Empleado", key="guardar_empleado_button"):
            create_employee(nombre_completo, cargo, departamento, pais, email, compania)
            st.success(f"Se ha agregado a {nombre_completo} como empleado.")

    elif section == "Eliminar Empleado":
        st.subheader("Eliminar Empleado")
        if os.path.exists(file):
            empleados = pd.read_csv(file)
            employee_options = ["Seleccionar empleado..."] + list(empleados['nombre completo'])
            #selected_employee = st.selectbox("Selecciona un empleado para eliminar:", employee_options)
            selected_employee = st.selectbox("Selecciona un empleado para eliminar:", employee_options, label_visibility='collapsed')

            if st.button("Eliminar", key="eliminar_button"):
                if selected_employee == "Seleccionar empleado...":
                    st.warning("Por favor, selecciona un empleado para eliminar.")
                else:
                    empleados = empleados[empleados['nombre completo'] != selected_employee]
                    empleados.to_csv(file, index=False)
                    st.success(f"Se ha eliminado a {selected_employee} como empleado.")
        else:
            st.warning("No hay empleados registrados para eliminar.")

