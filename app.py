import streamlit as st
import hashlib
import sqlite3
import pandas as pd

# Dados de usuário (substitua por um banco de dados real)
users = {
    "usuario1": hashlib.sha256("senha123".encode()).hexdigest(),
    "usuario2": hashlib.sha256("senha456".encode()).hexdigest(),
}

def login():
    st.title("Tela de Login")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if username in users and users[username] == hashed_password:
            st.success("Login realizado com sucesso!")
            return True  # Retorna True para indicar login bem-sucedido
        else:
            st.error("Usuário ou senha inválidos.")
    return False  # Retorna False para indicar login inválido

# Loop principal que só termina com login válido
logged_in = False
while not logged_in:
    logged_in = login() 

# Se chegar aqui, o login foi bem-sucedido
st.sidebar.title("Menu")
if st.sidebar.button("Opção 1"):
    st.write("Você selecionou a Opção 1")
if st.sidebar.button("Opção 2"):
    st.write("Você selecionou a Opção 2")

# ... outras opções do menu
