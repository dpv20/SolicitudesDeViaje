import os
import streamlit as st
import pandas as pd

def solicitudes_por_usuario(username):
    file = 'solicitudes_viaje.csv'
    st.title("Mis Solicitudes de Viaje")

    if username and os.path.exists(file):
        solicitudes = pd.read_csv(file)
        solicitudes.sort_values(by='solicitud', ascending=False, inplace=True)

        # Filter data for the entered username
        solicitudes_usuario = solicitudes[solicitudes['Nombre Empleado'] == username]

        if solicitudes_usuario.empty:
            st.warning("No hay solicitudes para el usuario especificado.")
        else:
            # Button to show dropdown and confirmation button
            if st.button("Anular una Solicitud"):
                st.session_state['show_dropdown'] = True

            if 'show_dropdown' in st.session_state and st.session_state['show_dropdown']:
                # Dropdown to select a solicitud to anular
                solicitud_to_anular = st.selectbox("Seleccione una solicitud para anular", 
                                                   solicitudes_usuario['solicitud'].unique())

                # Confirmation button
                if st.button("Confirmar Anulación"):
                    # Update the estado of the selected solicitud to 'anulado'
                    solicitudes.loc[solicitudes['solicitud'] == solicitud_to_anular, 'estado'] = 'anulado'
                    solicitudes.to_csv(file, index=False)
                    st.success(f"La solicitud {solicitud_to_anular} ha sido anulada.")

                    # Reset the state
                    st.session_state['show_dropdown'] = False

            # Display the solicitudes in a table
            st.markdown(solicitudes_usuario.to_html(index=False), unsafe_allow_html=True)

    elif not username:
        st.warning("Por favor, ingrese un nombre de usuario.")
    else:
        st.warning("No hay solicitudes registradas.")
