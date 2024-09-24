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
            # Libera o menu após a autenticação
            st.sidebar.title("Menu")
            st.sidebar.write("Agora você pode acessar as funcionalidades.")
            # Adicione as opções do menu aqui
            if st.sidebar.button("Opção 1"):
                st.write("Você selecionou a Opção 1")
            if st.sidebar.button("Opção 2"):
                st.write("Você selecionou a Opção 2")

            # ... outras opções do menu
        else:
            st.error("Usuário ou senha inválidos.")

# Bloqueia o menu inicialmente
st.sidebar.title("Menu")
st.sidebar.write("Faça login para desbloquear o menu.")
st.sidebar.write("")  # Adiciona um espaço em branco
st.sidebar.write("")  # Adiciona um espaço em branco
st.sidebar.write("")  # Adiciona um espaço em branco

if __name__ == "__main__":
    login()
