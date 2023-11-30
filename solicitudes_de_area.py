import pandas as pd
import streamlit as st
from pdf2image import convert_from_path
import base64
import os

def solicitudes_de_area(username):
    st.title(f"Solicitudes de Viaje")

    df_empleados = pd.read_csv("datos_empleados.csv")
    user_department_data = df_empleados[df_empleados['email'] == username]
    if user_department_data.empty:
        st.error("Usuario no encontrado en los datos de empleados.")
        return
    #print("holi")
    #print(st.session_state['user_role'])
    #print("holi")
    if username == "agonzalez@crystal-lagoons.com":
        departamento = st.session_state['user_position']
    else:
        departamento = user_department_data['departamento'].iloc[0]
    st.subheader(f"Departamento: {departamento}")

    df_solicitudes = pd.read_csv("solicitudes_viaje.csv", parse_dates=['fecha_solicitud'], dayfirst=True)
    estado_options = ["pendiente", "rechazado", "aprobado"]
    selected_estado = st.radio("Seleccione el estado de las solicitudes:", estado_options)

    filtered_solicitudes = df_solicitudes[(df_solicitudes['estado'] == selected_estado) & (df_solicitudes['departamento'] == departamento)]

    header_cols = st.columns([2, 2, 3, 2, 2])
    header_cols[0].write("Fecha")
    header_cols[1].write("Nombre Empleado")
    header_cols[2].write("Solicitud Número")
    header_cols[3].write("Estado")
    header_cols[4].write("Seleccionar")

    for index, row in filtered_solicitudes.iterrows():
        cols = st.columns([2, 2, 3, 2, 2])
        cols[0].write(row['fecha_solicitud'].strftime('%d/%m/%Y'))
        cols[1].write(row['Nombre Empleado'])
        cols[2].write(f"Solicitud número {row['solicitud']}")
        cols[3].write(row['estado'])

        select_button = cols[-1].button("Seleccionar", key=str(row['solicitud']))
        if select_button:
            st.session_state['selected_solicitud'] = row['solicitud']

    if 'selected_solicitud' in st.session_state:
        selected_solicitud = st.session_state['selected_solicitud']
        fecha_selected_solicitud = df_solicitudes.loc[df_solicitudes['solicitud'] == selected_solicitud, 'fecha_solicitud'].iloc[0]
        solicitud_filename = f"{fecha_selected_solicitud.strftime('%Y%m%d')}_{selected_solicitud}"

        pdf_path = os.path.join('formularios_viaje', f"{solicitud_filename}.pdf")
        if os.path.exists(pdf_path):
            images = convert_from_path(pdf_path)
            for image in images:
                st.image(image, width=1000)
        else:
            st.error("Error mostrando el PDF.")

        excel_path = os.path.join('formularios_viaje', f"{solicitud_filename}.xlsx")
        if os.path.exists(excel_path):
            with open(excel_path, 'rb') as file:
                excel_data = base64.b64encode(file.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{excel_data}" download="{solicitud_filename}.xlsx">Descargar Excel</a>'
                st.markdown(href, unsafe_allow_html=True)
        else:
            st.error("Error al descargar el archivo Excel.")

        img_path_png = os.path.join('formularios_viaje', f"{solicitud_filename}.png")
        img_path_jpg = os.path.join('formularios_viaje', f"{solicitud_filename}.jpg")
        
        if os.path.exists(img_path_png):
            img_path = img_path_png
        elif os.path.exists(img_path_jpg):
            img_path = img_path_jpg
        else:
            img_path = None

        if img_path:
            def toggle_image_display():
                if f'show_image_{selected_solicitud}' in st.session_state:
                    st.session_state[f'show_image_{selected_solicitud}'] = not st.session_state[f'show_image_{selected_solicitud}']
                else:
                    st.session_state[f'show_image_{selected_solicitud}'] = True

            toggle_button = st.button("Mostrar/Ocultar Imagen", key=f'toggle_image_{selected_solicitud}', on_click=toggle_image_display)

            if f'show_image_{selected_solicitud}' in st.session_state and st.session_state[f'show_image_{selected_solicitud}']:
                st.image(img_path, width=500)
        else:
            pass
            #st.error("Error al mostrar la imagen.")

        comentario = st.text_input("Dejar comentario (opcional):")
        approve_button = st.button("Aprobar")
        reject_button = st.button("Rechazar")

        if approve_button or reject_button:
            new_status = 'aprobado' if approve_button else 'rechazado'
            df_solicitudes.loc[df_solicitudes['solicitud'] == selected_solicitud, 'estado'] = new_status
            df_solicitudes.loc[df_solicitudes['solicitud'] == selected_solicitud, 'comentario'] = comentario
            df_solicitudes.to_csv("solicitudes_viaje.csv", index=False)
            st.success(f"Solicitud {selected_solicitud} ha sido {new_status}.")
