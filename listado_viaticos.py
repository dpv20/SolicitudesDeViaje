import os
import streamlit as st
import pandas as pd

def create_viatico(lugar, usd):
    new_viatico = pd.DataFrame([[lugar, usd]],
                               columns=['nombre del lugar', 'USD'])
    new_viatico.to_csv("datos_viaticos.csv", mode='a', header=False, index=False)

def modify_viatico(selected_lugar, new_usd):
    file = 'datos_viaticos.csv'
    viaticos = pd.read_csv(file)
    viaticos.loc[viaticos['nombre del lugar'] == selected_lugar, 'USD'] = new_usd
    viaticos.to_csv(file, index=False)

def listado_viaticos():
    file = 'datos_viaticos.csv'
    st.title("Datos Viáticos")

    # Section control
    #section = st.radio("", ["Mostrar Listado", "Agregar Viático", "Modificar Viático", "Eliminar Viático"])
    section = st.radio("Control de Sección", ["Mostrar Listado", "Agregar Viático", "Modificar Viático", "Eliminar Viático"], key="viaticos_control_section", label_visibility='collapsed')
    if section == "Mostrar Listado":
        if os.path.exists(file):
            viaticos = pd.read_csv(file)

            # Add Ordenar button
            if st.button("Ordenar", key="ordenar_viaticos"):
                viaticos.sort_values(by='nombre del lugar', inplace=True)
                viaticos.to_csv(file, index=False)
                st.success("Lista ordenada por nombre del lugar.")

            st.markdown(viaticos.to_html(index=False), unsafe_allow_html=True)
        else:
            st.warning("No hay viáticos registrados.")

    elif section == "Agregar Viático":
        st.subheader("Agregar Viático")
        lugar = st.text_input("Nombre del lugar:")
        usd = st.text_input("USD:")

        if st.button("Guardar Viático", key="guardar_viatico"):
            create_viatico(lugar, usd)
            st.success(f"Se ha agregado el viático para {lugar}.")

    elif section == "Eliminar Viático":
        st.subheader("Eliminar Viático")
        if os.path.exists(file):
            viaticos = pd.read_csv(file)
            viatico_options = ["Seleccionar viático..."] + list(viaticos['nombre del lugar'])
            #selected_viatico = st.selectbox("Selecciona un viático para eliminar:", viatico_options)
            selected_viatico = st.selectbox("Selecciona un viático para eliminar:", viatico_options, key="select_eliminar_viatico")
            if st.button("Eliminar", key="eliminar_viatico"):
                if selected_viatico == "Seleccionar viático...":
                    st.warning("Por favor, selecciona un viático para eliminar.")
                else:
                    viaticos = viaticos[viaticos['nombre del lugar'] != selected_viatico]
                    viaticos.to_csv(file, index=False)
                    st.success(f"Se ha eliminado el viático para {selected_viatico}.")
        else:
            st.warning("No hay viáticos registrados para eliminar.")

    elif section == "Modificar Viático":
        st.subheader("Modificar Viático")
        if os.path.exists(file):
            viaticos = pd.read_csv(file)
            viatico_options = ["Seleccionar viático..."] + list(viaticos['nombre del lugar'])
            #selected_viatico = st.selectbox("Selecciona un viático para modificar:", viatico_options)
            selected_viatico = st.selectbox("Selecciona un viático para modificar:", viatico_options, key="select_modificar_viatico")

            if selected_viatico != "Seleccionar viático...":
                new_usd = st.text_input(f"Ingrese el nuevo valor en USD para {selected_viatico}:")
                if st.button("Modificar", key="modificar_viatico"):
                    modify_viatico(selected_viatico, new_usd)
                    st.success(f"Se ha modificado el viático para {selected_viatico}.")
        else:
            st.warning("No hay viáticos registrados para modificar.")

