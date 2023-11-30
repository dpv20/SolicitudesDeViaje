import os
import pandas as pd
import streamlit as st

def make_checklist(username):
    
    # Cargar el archivo
    df = pd.read_csv("listado_proyectos.csv")
    
    # Seleccionar laguna
    lagunas = df["Project Name"].unique().tolist()
    selected_laguna = st.selectbox("Elige una laguna:", lagunas)
    
    # Seleccionar fecha
    fecha = st.date_input("Elige una fecha:")
    
    # Una vez seleccionada la laguna y fecha, mostrar el resto de las opciones
    st.write(f"Has seleccionado la laguna: {selected_laguna} para la fecha: {fecha}")

    options = [
        "Personal de la Laguna",
        "Operación Limpieza de fondo",
        "Operación Limpieza Manual",
        "Operación Filtro",
        "Operación de sistema de dosificación",
        "Operación de sistema de Recirculación",
        "Funcionamiento de Telemetría",
        "Operación de Skimmers",
        "Operación Ultrasonido",
        "Infraestructura",
        "Condición Liner",
        "Condición Visual Laguna",
        "Funcionamiento de Agua de relleno",
        "Nivel de la laguna",
        "Medidas de mitigación"
    ]

    fields = {
        "Personal de la Laguna": ["¿Operando todo bien?", "Cantidad", "Dotación incompleta", "Nota", "Comentario"]
    }

    col1, col2 = st.columns(2)

    choice = col1.radio("Elige una opción", options)

    if choice == "Personal de la Laguna":
        # Si el 'all_good' no está en el session_state, inicialízalo a True
        if 'all_good' not in st.session_state:
            st.session_state.all_good = True

        all_good = col2.checkbox("¿Operando todo bien?", value=st.session_state.all_good, on_change=lambda: setattr(st.session_state, 'all_good', not st.session_state.all_good))

        if all_good:
            # Resetear otros campos si el checkbox 'all_good' está marcado
            st.session_state["cantidad"] = ""
            st.session_state["nota"] = 1
            st.session_state["comentario"] = ""
        else:
            cantidad = col2.text_input("Cantidad", value=st.session_state.get("cantidad", ""))
            
            dotacion_incompleta = col2.checkbox("Dotación incompleta")
            
            prev_nota = st.session_state.get("nota", 1)
            nota_options = [1, 2, 3, 4]
            nota = col2.selectbox("Nota", nota_options, index=nota_options.index(prev_nota))

            # Detectar cambios en la nota
            if nota != prev_nota:
                st.session_state["nota"] = nota
                prev_nota = nota

            comentario = col2.text_input("Comentario", value=st.session_state.get("comentario", ""))

            # Actualizar el session_state con los valores actuales de los widgets
            st.session_state["cantidad"] = cantidad
            st.session_state["comentario"] = comentario