import streamlit as st
import hashlib
import sqlite3
import pandas as pd

# Dados de usuário (substitua por um banco de dados real)
users = {
    "usuario1": hashlib.sha256("senha123".encode()).hexdigest(),
    "usuario2": hashlib.sha256("senha456".encode()).hexdigest(),
}


# Inicializar o estado da sessão
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Criar os widgets de input fora do loop
if "username_input" not in st.session_state:
    st.session_state.username_input = st.text_input("Usuário")

if "password_input" not in st.session_state:
    st.session_state.password_input = st.text_input("Senha", type="password")

if "login_button" not in st.session_state:
    st.session_state.login_button = st.button("Entrar")


def login():
    st.title("Tela de Login")

    if st.session_state.login_button:
        hashed_password = hashlib.sha256(st.session_state.password_input.encode()).hexdigest()
        if st.session_state.username_input in users and users[st.session_state.username_input] == hashed_password:
            st.success("Login realizado com sucesso!")
            st.session_state.logged_in = True
        else:
            st.error("Usuário ou senha inválidos.")


def menu():
    if st.session_state.logged_in:
        st.sidebar.title("Menu")
        if st.sidebar.button("Opção 1"):
            st.write("Você selecionou a Opção 1")
        if st.sidebar.button("Opção 2"):
            st.write("Você selecionou a Opção 2")



# Loop que executa a função de login até que o usuário esteja logado
while not st.session_state.logged_in:
    login()
    menu()
