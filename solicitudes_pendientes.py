import pandas as pd
import streamlit as st
from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path
import base64
import os

def solicitudes_pendientes():
    st.title("Solicitudes de Viaje Pendientes")
    
    # Leer el archivo CSV
    # Asegurarse de que las fechas se lean correctamente
    df_solicitudes = pd.read_csv("solicitudes_viaje.csv", parse_dates=['fecha_solicitud'], dayfirst=True)
    
    # Si no hay una columna de comentario, agrégala
    if 'comentario' not in df_solicitudes.columns:
        df_solicitudes['comentario'] = ''
    
    df_solicitudes = df_solicitudes.iloc[::-1]

    # Mostrar los nombres de las columnas
    header_cols = st.columns([2, 2, 3, 2, 2])
    header_cols[0].write("Fecha")
    header_cols[1].write("Nombre Empleado")
    header_cols[2].write("Solicitud Número")
    header_cols[3].write("Estado")
    header_cols[4].write("Seleccionar")
    
    # Mostrar la tabla con las solicitudes pendientes
    for index, row in df_solicitudes.iterrows():
        solicitud = row['solicitud']
        fecha = row['fecha_solicitud'].strftime('%d/%m/%Y')
        numero = solicitud
        estado = row['estado']
        nombre_empleado = row['Nombre Empleado']
        
        cols = st.columns([2, 2, 3, 2, 2])
        cols[0].write(fecha)
        cols[1].write(nombre_empleado)
        cols[2].write(f"Solicitud número {numero}")
        cols[3].write(estado)
        
        select_button = cols[-1].button("Seleccionar", key=str(solicitud))
        if select_button:
            selected_solicitud = solicitud
            st.session_state['selected_solicitud'] = solicitud
        st.write("---")
    
    st.write("---")

    # Manejar la solicitud seleccionada
    if 'selected_solicitud' in st.session_state:
        selected_solicitud = st.session_state['selected_solicitud']
        fecha_selected_solicitud = df_solicitudes.loc[df_solicitudes['solicitud'] == selected_solicitud, 'fecha_solicitud'].iloc[0]
        # Construir el nombre del archivo en el formato YYYYMMDD_solicitud
        solicitud_filename = f"{fecha_selected_solicitud.strftime('%Y%m%d')}_{selected_solicitud}"


        # Mostrar el PDF asociado
        pdf_path = os.path.join('formularios_viaje', f"{solicitud_filename}.pdf")
        if os.path.exists(pdf_path):
            images = convert_from_path(pdf_path)
            for image in images:
                st.image(image, width=1000)
        else:
            st.error("Error mostrando el PDF.")

        # Botón para descargar el archivo Excel
        excel_path = os.path.join('formularios_viaje', f"{solicitud_filename}.xlsx")
        if os.path.exists(excel_path):
            with open(excel_path, 'rb') as file:
                excel_data = base64.b64encode(file.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{excel_data}" download="{solicitud_filename}.xlsx">Descargar Excel</a>'
                st.markdown(href, unsafe_allow_html=True)
        else:
            st.error("Error al descargar el archivo Excel.")

        def toggle_image_display():
            if f'show_image_{selected_solicitud}' in st.session_state:
                st.session_state[f'show_image_{selected_solicitud}'] = not st.session_state[f'show_image_{selected_solicitud}']
            else:
                st.session_state[f'show_image_{selected_solicitud}'] = True



        # Botón para visualizar la imagen (manejo para .png y .jpg)
        img_path_png = os.path.join('formularios_viaje', f"{solicitud_filename}.png")
        img_path_jpg = os.path.join('formularios_viaje', f"{solicitud_filename}.jpg")
        
        if os.path.exists(img_path_png):
            img_path = img_path_png
        elif os.path.exists(img_path_jpg):
            img_path = img_path_jpg
        else:
            img_path = None

        if img_path:
            toggle_button = st.button("Mostrar/Ocultar Imagen", key=f'toggle_image_{selected_solicitud}', on_click=toggle_image_display)
            
            if f'show_image_{selected_solicitud}' in st.session_state and st.session_state[f'show_image_{selected_solicitud}']:
                st.image(img_path, width=500)
                
            #href_img = f'<a href="{img_path}" target="_blank">Ver Imagen</a>'
            #st.markdown(href_img, unsafe_allow_html=True)
        else:
            pass
            #st.error("Error al mostrar la imagen.")

        # Comentario y botones de Aprobar y Rechazar
        comentario = st.text_input("Dejar comentario (opcional):")
        approve_button = st.button(f"Aprobar")
        reject_button = st.button(f"Rechazar")

        if approve_button or reject_button:
            if approve_button:
                new_status = 'aprobado'
            else:
                new_status = 'rechazado'

            # Actualizar el estado y el comentario en el DataFrame
            df_solicitudes.loc[df_solicitudes['solicitud'] == selected_solicitud, 'estado'] = new_status
            df_solicitudes.loc[df_solicitudes['solicitud'] == selected_solicitud, 'comentario'] = comentario

            # Guardar el DataFrame actualizado en el archivo CSV
            df_solicitudes.to_csv("solicitudes_viaje.csv", index=False)
            st.success(f"Solicitud {selected_solicitud} ha sido {new_status}.")

