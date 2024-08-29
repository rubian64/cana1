import streamlit as st
import sqlite3
import os

# Função para conectar ao banco de dados e criar a tabela se não existir
def init_db():
    conn = sqlite3.connect('vendas2.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS vendas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  sale_type TEXT,
                  customer_code TEXT,
                  product_type TEXT,
                  quantity INTEGER,
                  product_value REAL,
                  payment_method TEXT,
                  total_value REAL)''')
    conn.commit()
    return conn

# Função para inserir dados na tabela
def insert_data(conn, sale_type, customer_code, product_type, quantity, product_value, payment_method, total_value):
    c = conn.cursor()
    c.execute('''INSERT INTO vendas (sale_type, customer_code, product_type, quantity, product_value, payment_method, total_value)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', (sale_type, customer_code, product_type, quantity, product_value, payment_method, total_value))
    conn.commit()

# Título do app
st.title("Sistema de Venda")

# Criação dos campos do formulário
sale_type = st.radio("Tipo de Venda", ["Venda Galpão", "Venda Externa"])
customer_code = st.text_input("Código do Cliente")
product_type = st.radio("Tipo de Produto", ["saco 20 kg", "amarrado 20 kg"])
quantity = st.number_input("Quantidade", min_value=0, step=1, format="%d")
product_value = st.number_input("Valor do Produto (R$)", min_value=0.0, format="%f")
payment_method = st.radio("Forma de Pagamento", ["Pix", "Dinheiro"])

# Cálculo do valor total da operação
if quantity and product_value:
    total_value = quantity * product_value
else:
    total_value = 0

# Exibição do valor total da operação
st.write(f"Total da Operação: R$ {total_value:.2f}")

# Botão para enviar o formulário
if st.button("Enviar"):
    # Inicializa o banco de dados e a tabela
    conn = init_db()
    
    # Insere os dados na tabela
    insert_data(conn, sale_type, customer_code, product_type, quantity, product_value, payment_method, total_value)
    
    # Exibe os dados enviados
    st.write(f"Tipo de Venda: {sale_type}")
    st.write(f"Código do Cliente: {customer_code}")
    st.write(f"Tipo de Produto: {product_type}")
    st.write(f"Quantidade: {quantity}")
    st.write(f"Valor do Produto: R$ {product_value:.2f}")
    st.write(f"Forma de Pagamento: {payment_method}")
    st.write(f"Total da Operação: R$ {total_value:.2f}")
    
    # Fecha a conexão com o banco de dados
    conn.close()
    st.success("Dados inseridos com sucesso no banco de dados!")
