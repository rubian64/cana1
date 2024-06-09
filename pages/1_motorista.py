import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect('cana.db')
c = conn.cursor()

def criar_motorista(nome, telefone, endereco):
    c.execute('INSERT INTO motorista (nome, telefone, endereco) VALUES (?, ?, ?)',
              (nome, telefone, endereco))
    conn.commit()

def ler_motoristas():
    c.execute('SELECT * FROM motorista')
    dados = c.fetchall()
    return dados

def atualizar_motorista(idmotorista, nome, telefone, endereco):
    c.execute('UPDATE motorista SET nome = ?, telefone = ?, endereco = ? WHERE idmotorista = ?',
              (nome, telefone, endereco, idmotorista))
    conn.commit()

def deletar_motorista(idmotorista):
    c.execute('DELETE FROM motorista WHERE idmotorista = ?', (idmotorista,))
    conn.commit()

# Interface do Streamlit
def main():
    st.title("Motorista")
    st.sidebar.title("CANA EXPRESS")
    st.sidebar.subheader("Motorista")
    menu = ["Adicionar", "Listar", "Atualizar", "Apagar"]
    escolha = st.sidebar.selectbox("Menu", menu)

    if escolha == "Adicionar":
        st.subheader("Adicionar")
        with st.form(key='criar_motorista'):
            nome = st.text_input("Nome")
            telefone = st.text_input("Telefone")
            endereco = st.text_input("Endereço")
            submit_button = st.form_submit_button(label='Cadastrar')

        if submit_button:
            criar_motorista(nome, telefone, endereco)
            st.success("Motorista cadastrado com sucesso!")

    elif escolha == "Listar":
        st.subheader("Visualizar Motoristas")
        resultado = ler_motoristas()
        df = pd.DataFrame(resultado, columns=["ID", "Nome", "Telefone", "Endereço"])
        st.dataframe(df)

    elif escolha == "Atualizar":
        st.subheader("Atualizar Motorista")
        with st.form(key='atualizar_motorista'):
            idmotorista = st.number_input("ID do Motorista", min_value=1)
            nome = st.text_input("Nome")
            telefone = st.text_input("Telefone")
            endereco = st.text_input("Endereço")
            submit_button = st.form_submit_button(label='Atualizar')

        if submit_button:
            atualizar_motorista(idmotorista, nome, telefone, endereco)
            st.success("Motorista atualizado com sucesso!")

    elif escolha == "Apagar":
        st.subheader("Deletar Motorista")
        with st.form(key='deletar_motorista'):
            idmotorista = st.number_input("ID do Motorista", min_value=1)
            submit_button = st.form_submit_button(label='Deletar')

        if submit_button:
            deletar_motorista(idmotorista)
            st.success("Motorista deletado com sucesso!")

if __name__ == '__main__':
    main()
