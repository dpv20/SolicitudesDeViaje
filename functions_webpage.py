import os
import streamlit as st
import pandas as pd
from pathlib import Path
import json
import sqlite3
import uuid
import secrets
import string


from streamlit_lottie import st_lottie
from streamlit_extras.switch_page_button import switch_page
from streamlit.source_util import _on_pages_changed, get_pages

DEFAULT_PAGE = "Login.py"



def get_all_pages():
    default_pages = get_pages(DEFAULT_PAGE)

    pages_path = Path("pages.json")

    if pages_path.exists():
        saved_default_pages = json.loads(pages_path.read_text())
    else:
        saved_default_pages = default_pages.copy()
        pages_path.write_text(json.dumps(default_pages, indent=4))

def clear_all_but_first_page():
    current_pages = get_pages(DEFAULT_PAGE)

    if len(current_pages.keys()) == 1:
        return

    get_all_pages()

    # Remove all but the first page
    key, val = list(current_pages.items())[0]
    current_pages.clear()
    current_pages[key] = val

    _on_pages_changed.send()

# Load users and passwords from CSV file
def load_users(file):
    data = pd.read_csv(file)
    users = {}
    for index, row in data.iterrows():
        users[row['username']] = {
            'password': row['password'],
            'role': row['role'],
            'position':row['position']
        }
    return users

users = load_users("users.csv")
def authenticate(username, password, users):
    if username in users and users[username]['password'] == password:
        return users[username]['role']
    return None

def login_page():
    st.title("Login Page")

    # Initialize a flag in session state if not already present
    if 'login_attempt' not in st.session_state:
        st.session_state['login_attempt'] = False

    username = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")
    submit_button = st.button("Login")

    # Check if the login button was clicked or if an attempt was already made
    if submit_button or st.session_state['login_attempt']:
        user_role = authenticate(username, password, users)
        if user_role:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['user_role'] = user_role
            st.session_state['login_attempt'] = False  # Reset the flag
        else:
            st.error("Invalid username or password")
            st.session_state['login_attempt'] = not submit_button
            # Only set the flag if the login button wasn't clicked this time



def create_user(username, password, role, position):
    users[username] = {
        'password': password,
        'role': role,
        'position': position
    }
    # Save new user to the CSV file
    new_user = pd.DataFrame([[username, password, role, position]], columns=['username', 'password', 'role', 'position'])
    new_user.to_csv("users.csv", mode='a', header=False, index=False)

def nuevo_usuario():
    #st.title("Admin Page")
    st.title("Crear nuevo usuario")
    new_username = st.text_input("New username")
    new_password = st.text_input("New password", type="password")
    new_role = st.selectbox("Role", ["user", "admin"])
    new_position = st.selectbox("Role", ["empleado", "director"])

    if st.button("Create user"):
        create_user(new_username, new_password, new_role, new_position)
        st.success(f"User {new_username} created")
        st.success(f"password: \"{new_password}\"")
        st.success(f"role: {new_role}")
        st.success(f"role: {new_position}")

def display_grid(users):
    # Display users as a grid
    st.write("<h2>Users</h2>", unsafe_allow_html=True)
    data = pd.DataFrame.from_dict(users, orient='index', columns=['password', 'role','position'])
    data.index.name = 'Username'
    st.write(data)

def display_users(users, file):
    #st.title("Users config")
    # Display user grid
    display_grid(users)

    # Delete user section
    st.write("## Delete User")
    delete_username = st.text_input("Username to delete")
    delete_password = st.text_input("Password", type="password")
    if st.button("Delete User"):
        if delete_username in users:
            if delete_password == users[delete_username]['password']:
                # Remove user from dictionary
                del users[delete_username]
                # Update CSV file
                data = pd.DataFrame.from_dict(users, orient='index', columns=['password', 'role','position'])
                data.index.name = 'username'
                data.to_csv(file, index_label='username')
                # Show success message
                st.success(f"User {delete_username} deleted successfully.")
                # Update user grid
            else:
                st.error("Invalid password.")
        else:
            st.error(f"User {delete_username} not found.")

def save_users(users):
    data = pd.DataFrame([(username, info['password'], info['role']) for username, info in users.items()],
                        columns=['username', 'password', 'role'])
    data.to_csv("users.csv", mode='w', header=True, index=False)
'''
def calculate_machine_rooms(area):
    machine_rooms = {"XS": 0, "S": 0, "M": 0, "L": 0}
    
    while area > 0:
        if area > 3.5:
            machine_rooms["L"] += 1
            area -= 7
        elif 3.5 >= area > 1.5:
            machine_rooms["M"] += 1
            area -= 3.5
        elif 1.5 >= area > 1:
            machine_rooms["S"] += 1
            area -= 1.5
        else:
            machine_rooms["XS"] += 1
            area -= 1
    
    return machine_rooms
'''



def format_labeled_answers(d):
    formatted_items = [f"{k}: {v}" for k, v in d.items()]
    return "{\n" + ",\n".join(formatted_items) + "\n}"

def generate_random_string(length=10):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
