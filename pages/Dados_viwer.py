import streamlit as st
import sqlite3
import pandas as pd

# Conectar ao banco de dados SQLite
def connect_to_db(db_name):
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Obter a lista de tabelas no banco de dados
def get_tables(conn):
    try:
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        cursor = conn.execute(query)
        tables = [row[0] for row in cursor.fetchall()]
        return tables
    except sqlite3.Error as e:
        st.error(f"Erro ao obter a lista de tabelas: {e}")
        return []

# Obter os dados de uma tabela específica
def get_table_data(conn, table_name):
    try:
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql(query, conn)
        return df
    except sqlite3.Error as e:
        st.error(f"Erro ao obter dados da tabela: {e}")
        return pd.DataFrame()

# Lista de bancos de dados SQLite
databases = ["usuarios.db", "motoristas.db", "clientes.db","vendas2.db"]

# Título do aplicativo Streamlit
st.title("Visualizador de Bancos de Dados SQLite")

# Selecionar um banco de dados
selected_db = st.selectbox("Escolha um banco de dados para visualizar", databases)

# Conectar ao banco de dados selecionado
conn = connect_to_db(selected_db)

if conn is not None:
    # Obter a lista de tabelas
    tables = get_tables(conn)
    
    if tables:
        # Selecionar uma tabela para visualizar
        selected_table = st.selectbox("Escolha uma tabela para visualizar", tables)
        
        if selected_table:
            # Exibir os dados da tabela selecionada
            st.write(f"Tabela selecionada: {selected_table}")
            table_data = get_table_data(conn, selected_table)
            st.dataframe(table_data)
    else:
        st.warning("Nenhuma tabela encontrada no banco de dados.")

    # Fechar a conexão com o banco de dados
    conn.close()
else:
    st.error("Falha ao conectar ao banco de dados.")
