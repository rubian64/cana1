import streamlit as st
import sqlite3
import pandas as pd

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('clientes.db')
c = conn.cursor()

# Criação da tabela de clientes
c.execute('''
          CREATE TABLE IF NOT EXISTS cliente (
            idcliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            endereco TEXT,
            telefone TEXT,
            cnpj TEXT,
            cpf TEXT,
            email TEXT,
            tipo TEXT
          )
          ''')
conn.commit()

# Funções CRUD
def criar_cliente(nome, endereco, telefone, cnpj, cpf, email, tipo):
    c.execute('INSERT INTO cliente (nome, endereco, telefone, cnpj, cpf, email, tipo) VALUES (?, ?, ?, ?, ?, ?, ?)',
              (nome, endereco, telefone, cnpj, cpf, email, tipo))
    conn.commit()

def ler_clientes():
    c.execute('SELECT * FROM cliente')
    dados = c.fetchall()
    return dados

def atualizar_cliente(idcliente, nome, endereco, telefone, cnpj, cpf, email, tipo):
    c.execute('UPDATE cliente SET nome = ?, endereco = ?, telefone = ?, cnpj = ?, cpf = ?, email = ?, tipo = ? WHERE idcliente = ?',
              (nome, endereco, telefone, cnpj, cpf, email, tipo, idcliente))
    conn.commit()

def deletar_cliente(idcliente):
    c.execute('DELETE FROM cliente WHERE idcliente = ?', (idcliente,))
    conn.commit()

# Interface do Streamlit
def main():
    st.title("Cadastro de Cliente - CANA EXPRESS")

    menu = ["Criar", "Ler", "Atualizar", "Deletar"]
    escolha = st.sidebar.selectbox("Menu", menu)

    if escolha == "Criar":
        st.subheader("Adicionar Novo Cliente")
        with st.form(key='criar_cliente'):
            nome = st.text_input("Nome")
            endereco = st.text_input("Endereco")
            telefone = st.text_input("Telefone")
            cnpj = st.text_input("CNPJ")
            cpf = st.text_input("CPF")
            email = st.text_input("Email")
            tipo = st.selectbox("Tipo", ["E", "P"])  # E para Empresa, P para Particular
            submit_button = st.form_submit_button(label='Cadastrar')

        if submit_button:
            criar_cliente(nome, endereco, telefone, cnpj, cpf, email, tipo)
            st.success("Cliente cadastrado com sucesso!")

    elif escolha == "Ler":
        st.subheader("Visualizar Clientes")
        resultado = ler_clientes()
        df = pd.DataFrame(resultado, columns=["ID", "Nome", "Endereco", "Telefone", "cnpj", "cpf", "Email", "Tipo"])
        st.dataframe(df)

    elif escolha == "Atualizar":
        st.subheader("Atualizar Cliente")
        with st.form(key='atualizar_cliente'):
            idcliente = st.number_input("ID do Cliente", min_value=1)
            nome = st.text_input("Nome")
            endereco = st.text_input("Endereco")
            telefone = st.text_input("Telefone")
            cnpj = st.text_input("CNPJ")
            cpf = st.text_input("cpf")
            email = st.text_input("Email")
            tipo = st.selectbox("Tipo", ["E", "P"])  # E para Empresa, P para Particular
            submit_button = st.form_submit_button(label='Atualizar')

        if submit_button:
            atualizar_cliente(idcliente, nome, endereco, telefone, cnpj, cpf, email, tipo)
            st.success("Cliente atualizado com sucesso!")

    elif escolha == "Deletar":
        st.subheader("Deletar Cliente")
        with st.form(key='deletar_cliente'):
            idcliente = st.number_input("ID do Cliente", min_value=1)
            submit_button = st.form_submit_button(label='Deletar')

        if submit_button:
            deletar_cliente(idcliente)
            st.success("Cliente deletado com sucesso!")

if __name__ == '__main__':
    main()
