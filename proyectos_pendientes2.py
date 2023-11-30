import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import shutil
from typing import List
import datetime
import os
import win32com.client as win32
import pythoncom
from PyPDF2 import PdfWriter, PdfReader, PdfMerger
from functions_webpage import *
import datetime
import secrets
import string


import os
from pdf2image import convert_from_path
from shutil import copyfileobj
import base64
from io import BytesIO


from send_mail import *

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

def replace_word_in_file(tag, old_word, new_word):
    file_path = os.path.join('TEXs', tag, tag + '.txt')
    with open(file_path, 'r') as f:
        content = f.read()

    content = content.replace(old_word, new_word)

    with open(file_path, 'w') as f:
        f.write(content)






def proyectos_pendientes():
    st.title("Pendiente Projects")
    df_proyectos = pd.read_csv("proyectos.csv")

    # Filter the data to show only the projects with "pendiente" status
    pendiente_projects = df_proyectos[df_proyectos["Estado"] == "pendiente"]

    selected_columns = ["Project Name", "Country", "Date", "Estado", "Username"]
    header_columns = st.columns([3, 2, 2, 2, 3, 2])  # Adjust column widths here

    for col, field_name in zip(header_columns, selected_columns):
        col.write(field_name)

    header_columns[-1].write("Select TAG")

    selected_tag = None

    for _, row in pendiente_projects.iterrows():
        row_columns = st.columns([3, 2, 2, 2, 3, 2])  # Adjust column widths here

        for col, field_name in zip(row_columns, selected_columns):
            col.write(row[field_name])

        button_phold = row_columns[-1].empty()
        select_button = button_phold.button("Select", key=row["TAG"])
        if select_button:
            selected_tag = row["TAG"]
    
        st.write("---")  # Add a horizontal line between rows

    # Display the PDF corresponding to the selected row
    if selected_tag:
        pdf_path = os.path.join("TEXs", selected_tag, f"{selected_tag}.pdf")
        txt_path = os.path.join("TEXs", selected_tag, f"{selected_tag}.txt")
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as file:
                txt_content = file.read()
            st.text(txt_content)
        else:
            st.error("Error displaying the text file.")
        if os.path.exists(pdf_path):
            images = convert_from_path(pdf_path)
            for image in images:
                with st.container():
                    st.markdown(
                        f"<style>.center-image {{ display: block; margin-left: auto; margin-right: auto;}}</style>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="center-image"><img src="data:image/png;base64,{image_to_base64(image)}" width="1000"></div>',
                        unsafe_allow_html=True,
                    )
        else:
            st.error("Error displaying the PDF.")
    
    # Function to replace the existing PDF with a new one
    def replace_pdf(selected_tag, uploaded_pdf):
        if uploaded_pdf is not None:
            with open(f"TEXs/{selected_tag}.pdf", "wb") as f:
                copyfileobj(uploaded_pdf, f)
            st.success(f"PDF for {selected_tag} has been replaced successfully.")
            return True

        return False

    uploaded_pdf = st.file_uploader("Upload a new PDF", type=["pdf"])

    if uploaded_pdf:
        if replace_pdf(selected_tag, uploaded_pdf):
            # If the PDF was replaced, re-read it from the file and display the new one
            pdf_path = os.path.join("TEXs", f"{selected_tag}.pdf")
            if os.path.exists(pdf_path):
                images = convert_from_path(pdf_path)
                for image in images:
                    st.image(image, width=1000)
            else:
                st.error("Error displaying the replaced PDF.")
    
    def update_project_status(tag, new_status, comment=None):
        df_proyectos.loc[df_proyectos['TAG'] == tag, 'Estado'] = new_status
        df_proyectos.to_csv("proyectos.csv", index=False)
        st.success(f"Project with TAG {tag} has been {new_status}.")
        
        if new_status == 'rechazado' and comment:
            with open(f"coments/{tag}.txt", "w") as f:
                f.write(comment)



    # Save selected_tag in session_state
    if selected_tag:
        st.session_state['selected_tag'] = selected_tag
    
    if 'selected_tag' in st.session_state:
        project_name = df_proyectos[df_proyectos["TAG"] == st.session_state['selected_tag']]["Project Name"].values[0]
        comment = st.text_input("Enter a comment (optional)")
        add_comment_button = st.button("Agregar comentario")

        if add_comment_button:
            txt_path = os.path.join("TEXs", st.session_state['selected_tag'], f"{st.session_state['selected_tag']}.txt")
            if os.path.exists(txt_path):
                with open(txt_path, 'a') as file:  # 'a' stands for append
                    file.write("\n"+"\n" + "Comentario:" + "\n" + comment)  # write the comment to a new line
                st.success("Your comment has been added.")
            else:
                st.error("The text file does not exist.")

        st.write("--------------------------------")



        st.write("Advertencia: Agregue un comentario antes de seleccionar una opcion si desea agregarlo")
        approve_button = st.button(f"Aprobar el PDF")
        reject_button = st.button(f"Rechazar el PDF")

        if approve_button:
            st.write("Approve button clicked")  # Debugging print
            update_project_status(st.session_state['selected_tag'], 'aprobado')
            replace_word_in_file(st.session_state['selected_tag'], 'pendiente', 'aprobado')  # Add this line
            send_mail(f'{project_name} approved', st.session_state['selected_tag'])
        elif reject_button:
            st.write("Reject button clicked")  # Debugging print
            update_project_status(st.session_state['selected_tag'], 'rechazado')
            replace_word_in_file(st.session_state['selected_tag'], 'pendiente', 'rechazado')  # Add this line
            send_mail(f'{project_name} rejected', st.session_state['selected_tag'], attach_pdf=False)