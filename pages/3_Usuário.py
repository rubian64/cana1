import sqlite3
import streamlit as st
import pandas as pd

conn = sqlite3.connect('cana.db')
cursor = conn.cursor()

def create_user(login, senha, email, tipo):
    cursor.execute('''
    INSERT INTO usuario (login, senha, email, tipo) VALUES (?, ?, ?, ?)
    ''', (login, senha, email, tipo))
    conn.commit()

def read_users():
    cursor.execute('SELECT * FROM usuario')
    users = cursor.fetchall()
    return users

def update_user(idusuario, login, senha, email, tipo):
    
    cursor.execute('''
    UPDATE usuario SET login = ?, senha = ?, email = ?, tipo = ? WHERE idusuario = ?
    ''', (login, senha, email, tipo, idusuario))
    conn.commit()

def delete_user(idusuario):
    conn = sqlite3.connect('cana.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuario WHERE idusuario = ?', (idusuario,))
    conn.commit()

def main():
    st.title("Usuário")
    st.sidebar.title("CANA EXPRESS")
    st.sidebar.subheader("Usuário")

    menu = ["Adicionar", "Listar", "Atualizar", "Apagar"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Adicionar":
        st.subheader("Adicionar")
        with st.form(key="Adicionar"):
            login = st.text_input("Login")
            senha = st.text_input("Senha", type="password")
            email = st.text_input("Email")
            tipo = st.selectbox(label="Tipo", options=["Motorista", "Gestão"])
            if st.form_submit_button("Adicionar"):
                create_user(login, senha, email, tipo)
                st.success(f"Usuário {login} adicionado com sucesso")

    elif choice == "Listar":
        st.subheader("Listar")
        users = read_users()
        df = pd.DataFrame(users, columns=["ID", "login", "senha", "email", "tipo"])
        st.dataframe(df)

    elif choice == "Atualizar":
        st.subheader("Atualizar")
        idusuario = st.number_input("ID do Usuário", min_value=1)
        login = st.text_input("Login")
        senha = st.text_input("Senha", type="password")
        email = st.text_input("Email")
        tipo = st.selectbox("Tipo", ["M", "G"])  # M para Motorista, G para Gestão
        if st.button("Atualizar"):
            update_user(idusuario, login, senha, email, tipo)
            st.success(f"Usuário {idusuario} atualizado com sucesso")

    elif choice == "Apagar":
        st.subheader("Apagar")
        idusuario = st.number_input("ID do Usuário", min_value=1)
        if st.button("Deletar"):
            delete_user(idusuario)
            st.success(f"Usuário {idusuario} deletado com sucesso")

if __name__ == '__main__':
    main()
