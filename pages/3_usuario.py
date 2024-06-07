import sqlite3
import streamlit as st

# Configuração do banco de dados
def init_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuario (
        idusuario INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT,
        senha TEXT,
        email TEXT,
        tipo TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Funções CRUD
def create_user(login, senha, email, tipo):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO usuario (login, senha, email, tipo) VALUES (?, ?, ?, ?)
    ''', (login, senha, email, tipo))
    conn.commit()
    conn.close()

def read_users():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuario')
    users = cursor.fetchall()
    conn.close()
    return users

def update_user(idusuario, login, senha, email, tipo):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE usuario SET login = ?, senha = ?, email = ?, tipo = ? WHERE idusuario = ?
    ''', (login, senha, email, tipo, idusuario))
    conn.commit()
    conn.close()

def delete_user(idusuario):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuario WHERE idusuario = ?', (idusuario,))
    conn.commit()
    conn.close()

# Interface do Streamlit
def main():
    st.title("CRUD de Usuários com Streamlit e SQLite")

    menu = ["Create", "Read", "Update", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)

    init_db()

    if choice == "Create":
        st.subheader("Adicionar Usuário")
        login = st.text_input("Login")
        senha = st.text_input("Senha", type="password")
        email = st.text_input("Email")
        tipo = st.selectbox("Tipo", ["M", "G"])  # M para Motorista, G para Gestão
        if st.button("Adicionar"):
            create_user(login, senha, email, tipo)
            st.success(f"Usuário {login} adicionado com sucesso")

    elif choice == "Read":
        st.subheader("Lista de Usuários")
        users = read_users()
        for user in users:
            st.write(user)

    elif choice == "Update":
        st.subheader("Atualizar Usuário")
        idusuario = st.number_input("ID do Usuário", min_value=1)
        login = st.text_input("Login")
        senha = st.text_input("Senha", type="password")
        email = st.text_input("Email")
        tipo = st.selectbox("Tipo", ["M", "G"])  # M para Motorista, G para Gestão
        if st.button("Atualizar"):
            update_user(idusuario, login, senha, email, tipo)
            st.success(f"Usuário {idusuario} atualizado com sucesso")

    elif choice == "Delete":
        st.subheader("Deletar Usuário")
        idusuario = st.number_input("ID do Usuário", min_value=1)
        if st.button("Deletar"):
            delete_user(idusuario)
            st.success(f"Usuário {idusuario} deletado com sucesso")

if __name__ == '__main__':
    main()
