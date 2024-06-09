import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect('cana.db')

# Função para exibir a tabela motorista
def display_motorista():
    st.subheader('Motoristas')
    query = "SELECT * FROM motorista"
    motoristas = pd.read_sql(query, conn)
    st.dataframe(motoristas)

# Função para exibir a tabela entrega
def display_entrega():
    st.subheader('Entregas')
    query = "SELECT * FROM entrega"
    entregas = pd.read_sql(query, conn)
    st.dataframe(entregas)

def add_motorista():
    st.subheader('Adicionar Motorista')
    idmotorista = st.number_input('ID do Motorista', min_value=1, step=1)
    nome = st.text_input('Nome')
    telefone = st.text_input('Telefone')
    endereco = st.text_input('Endereço')
    if st.button('Adicionar Motorista'):
        with conn:
            conn.execute('INSERT INTO motorista (idmotorista, nome, telefone, endereco) VALUES (?, ?, ?, ?)',
                         (idmotorista, nome, telefone, endereco))
        st.success('Motorista adicionado com sucesso!')

# Função para adicionar nova entrega
def add_entrega():
    st.subheader('Adicionar Entrega')
    identrega = st.number_input('ID da Entrega', min_value=1, step=1)
    turno = st.text_input('Turno')
    datahora_retirada = st.text_input('Data/Hora Retirada')
    datahora_entrega = st.text_input('Data/Hora Entrega')
    motorista_idmotorista = st.number_input('ID do Motorista', min_value=1, step=1)
    if st.button('Adicionar Entrega'):
        with conn:
            conn.execute('INSERT INTO entrega (identrega, turno, datahora_retirada, datahora_entrega, motorista_idmotorista) VALUES (?, ?, ?, ?, ?)',
                         (identrega, turno, datahora_retirada, datahora_entrega, motorista_idmotorista))
        st.success('Entrega adicionada com sucesso!')

# Interface Streamlit
st.title('Gestão de Entregas')
st.sidebar.title("CANA EXPRESS")
st.sidebar.subheader("Entregas")

#menu = ['Ver Motoristas', 'Ver Entregas', 'Adicionar Motorista', 'Adicionar Entrega']
menu = ['Ver Entregas', 'Adicionar Entrega']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'Ver Motoristas':
    display_motorista()
elif choice == 'Ver Entregas':
    display_entrega()
elif choice == 'Adicionar Motorista':
    add_motorista()
elif choice == 'Adicionar Entrega':
    add_entrega()

# Fechar a conexão ao banco de dados ao final
conn.close()
