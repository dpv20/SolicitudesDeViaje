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

def modify_solicitud(selected_solicitud, new_data):
    file = 'solicitudes_viaje.csv'
    solicitudes = pd.read_csv(file)
    for column in new_data:
        if column != 'solicitud':
            solicitudes.loc[solicitudes['solicitud'] == selected_solicitud, column] = new_data[column]
    solicitudes.to_csv(file, index=False)


def solicitudes_aprobadas():
    file = 'solicitudes_viaje.csv'
    st.title("Solicitudes de Viaje")
    
    # Section control
    section = st.radio("", ["Mostrar Listado", "Modificar Solicitud", "Eliminar Solicitud"])
    
    if os.path.exists(file):
        solicitudes = pd.read_csv(file)
        
        if section == "Mostrar Listado":
            # Filter the data to show only 'aprobado' estado
            solicitudes_aprobado = solicitudes[solicitudes['estado'] == 'aprobado']
            
            if solicitudes_aprobado.empty:
                st.warning("No hay solicitudes aprobadas.")
            else:
                st.markdown(solicitudes_aprobado.to_html(index=False), unsafe_allow_html=True)
    
        elif section == "Modificar Solicitud":
            st.subheader("Modificar Solicitud")
            
            # Filter the data to list only 'aprobado' estado
            solicitudes_pendiente = solicitudes[solicitudes['estado'] == 'aprobado']
            solicitudes_list = solicitudes_pendiente['solicitud'].tolist()
            
            selected_solicitud = st.selectbox("Seleccione una solicitud para modificar:", [""] + solicitudes_list)
            
            if selected_solicitud:
                selected_data = solicitudes[solicitudes['solicitud'] == selected_solicitud].iloc[0]
                
                # Solicitud number should not be modifiable
                st.write("Solicitud:", selected_data['solicitud'])
                
                # Fields that can be modified
                nombre_empleado = st.text_input("Nombre Empleado:", value=selected_data['Nombre Empleado'])
                departamento = st.text_input("Departamento:", value=selected_data['departamento'])
                total_usd_viatico = st.number_input("Total USD Viático:", value=selected_data['total_usd_viatico'])
                fecha_partida = st.date_input("Fecha de Partida:", value=pd.to_datetime(selected_data['fecha_partida']))
                fecha_llegada = st.date_input("Fecha de Llegada:", value=pd.to_datetime(selected_data['fecha_llegada']))
                comentario = st.text_area("Comentario:", value=selected_data['comentario'])
                
                if st.button("Guardar Cambios"):
                    solicitudes.loc[solicitudes['solicitud'] == selected_solicitud, 'Nombre Empleado'] = nombre_empleado
                    solicitudes.loc[solicitudes['solicitud'] == selected_solicitud, 'departamento'] = departamento
                    solicitudes.loc[solicitudes['solicitud'] == selected_solicitud, 'total_usd_viatico'] = total_usd_viatico
                    solicitudes.loc[solicitudes['solicitud'] == selected_solicitud, 'fecha_partida'] = fecha_partida
                    solicitudes.loc[solicitudes['solicitud'] == selected_solicitud, 'fecha_llegada'] = fecha_llegada
                    solicitudes.loc[solicitudes['solicitud'] == selected_solicitud, 'comentario'] = comentario
                    solicitudes.to_csv(file, index=False)
                    st.success(f"Se ha modificado la solicitud {selected_solicitud}.")
            
        elif section == "Eliminar Solicitud":
            st.subheader("Eliminar Solicitud")
            solicitudes_pendiente = solicitudes[solicitudes['estado'] == 'aprobado']
            solicitudes_list = solicitudes_pendiente['solicitud'].tolist()
            
            selected_solicitud = st.selectbox("Seleccione una solicitud para eliminar:", [""] + solicitudes_list)
            
            if st.button("Eliminar"):
                if selected_solicitud:
                    solicitudes = solicitudes[solicitudes['solicitud'] != selected_solicitud]
                    solicitudes.to_csv(file, index=False)
                    st.success(f"Se ha eliminado la solicitud {selected_solicitud}.")
                else:
                    st.warning("Por favor, selecciona una solicitud para eliminar.")
                    
    else:
        st.warning("No hay solicitudes registradas.")