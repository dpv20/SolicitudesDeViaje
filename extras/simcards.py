import os
import streamlit as st
import pandas as pd
from twilio.rest import Client


def create_simcard(name, sim_sid):
    simcards_file = 'extras/simcards.csv'
    new_simcard = pd.DataFrame([[name, sim_sid]],
                               columns=['name', 'sim_sid'])
    new_simcard.to_csv(simcards_file, mode='a', header=False, index=False)



def enviar_SMS(sim_sid, message):
    account_sid = 'AC3903e3c46f762af37900a7946f301223'
    auth_token = 'c245e882ece4c2664dcca16515174b3c'
    client = Client(account_sid, auth_token)
    command = client.wireless.v1.commands.create(
        sim = sim_sid,
        command = message
    )

def simcards():
    simcards_file = 'extras/simcards.csv'
    if os.path.exists(simcards_file):
        simcards = pd.read_csv(simcards_file)
        st.title("Send Message to SIM Card")

        # Dropdown for selecting SIM card
        simcard_names = list(simcards['name'])
        selected_name = st.selectbox("Select a SIM Card:", [""] + simcard_names)

        # Check if a SIM card is selected
        if selected_name:
            # Text field for the message
            message = st.text_area("Message")

            if st.button("Send"):
                # Retrieve the SID for the selected SIM card
                selected_sid = simcards[simcards['name'] == selected_name]['sim_sid'].iloc[0]
                enviar_SMS(selected_sid, message)
                st.success(f"Message '{message}' was sent to the SIM card '{selected_name}' with SID '{selected_sid}'.")
        else:
            st.write("Please select a SIM card to send a message.")
    else:
        st.error("No SIM cards found.")


def newsimcard():
    st.title("SIM Card Management")
    simcards_file = 'extras/simcards.csv'
    section = st.radio("Select an action", ["List SIM Cards", "Add SIM Card", "Delete SIM Card"], label_visibility='collapsed')

    if section == "List SIM Cards":
        if os.path.exists(simcards_file):
            simcards = pd.read_csv(simcards_file)
            st.markdown(simcards.to_html(index=False), unsafe_allow_html=True)
        else:
            st.warning("No SIM cards registered.")

    elif section == "Add SIM Card":
        st.subheader("Add a New SIM Card")
        name = st.text_input("SIM Card Name:")
        sim_sid = st.text_input("SIM SID:")

        if st.button("Save SIM Card", key="save_simcard_button"):
            create_simcard(name, sim_sid)
            st.success(f"SIM card '{name}' added successfully.")


    elif section == "Delete SIM Card":
        st.subheader("Delete a SIM Card")
        if os.path.exists(simcards_file):
            simcards = pd.read_csv(simcards_file)
            simcard_options = ["Select a SIM card..."] + list(simcards['name'])
            selected_simcard = st.selectbox("Select a SIM card to delete:", simcard_options, label_visibility='collapsed')

            if st.button("Delete", key="delete_simcard_button"):
                if selected_simcard == "Select a SIM card...":
                    st.warning("Please select a SIM card to delete.")
                else:
                    simcards = simcards[simcards['name'] != selected_simcard]
                    simcards.to_csv(simcards_file, index=False)
                    st.success(f"SIM card '{selected_simcard}' deleted successfully.")
        else:
            st.warning("No SIM cards registered to delete.")