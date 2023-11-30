import streamlit as st
import time
from moviepy.editor import *
from streamlit import components



def homepage():
    
    #st.title("Your Streamlit App with a Video Background")


    # Load original GIF file
    #original_gif = VideoFileClip("media/gifs/crystal.gif")

    # Extract portion of GIF from 0 to 3.95 seconds
    #trimmed_gif = original_gif.subclip(0, 3.95)

    # Save trimmed GIF to a new file
    #trimmed_gif.write_gif("media/gifs/crystal_trimmed.gif")


    #with open('media/gifs/crystal.gif', 'rb') as f: 
        #st.image(f.read())

    vimeo_video_id = "809122136"
    components.v1.iframe(f"https://player.vimeo.com/video/{vimeo_video_id}?autoplay=1&loop=1&background=1", width=640, height=360)




    st.write("Dirijase al menu del costado izquierdo para seleccionar la opcion que corresponda")
    st.write("Solicitud de TEX")
    st.subheader("App Features actuales")
    st.write("Solicitud de TEX")
    #st.write("- Project management")
    #st.write("- Survey creation and analysis")
    #st.write("- Contact management")

    #st.subheader("About the Developer")
    #st.write("This app was developed by Diego Pavez, a software engineer of Crystal lagoons.")



#st.sidebar.title('Menu')
#choice = st.sidebar.selectbox("Menu", ["homepage", "projects", "surveys", "contacts","diego","diego2"])

#homepage()