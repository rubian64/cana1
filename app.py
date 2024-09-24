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
            # Redirecionar para a área de cliente
            st.write("Bem-vindo(a),", username)
        else:
            st.error("Usuário ou senha inválidos.")


if __name__ == "__main__":
    login()
