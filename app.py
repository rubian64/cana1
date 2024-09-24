import streamlit as st
import hashlib
import sqlite3
import pandas as pd

# Dados de usuário (substitua por um banco de dados real)
users = {
    "usuario1": hashlib.sha256("senha123".encode()).hexdigest(),
    "usuario2": hashlib.sha256("senha456".encode()).hexdigest(),
}

# Inicializar o estado de sessão
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("Tela de Login")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if username in
