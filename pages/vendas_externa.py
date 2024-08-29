import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import requests
from fpdf import FPDF
import io

# Função para obter coordenadas a partir de um endereço usando a API do Google Maps
def obter_coordenadas(endereco):
    # Substitua 'YOUR_API_KEY' pela sua chave de API do Google Maps
    api_key = 'YOUR_API_KEY'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={endereco}&key={api_key}'
    response = requests.get(url)
    dados = response.json()
    
    if dados['status'] == 'OK':
        coordenadas = dados['results'][0]['geometry']['location']
        return coordenadas['lat'], coordenadas['lng']
    else:
        st.error("Não foi possível obter coordenadas para o endereço fornecido.")
        return None, None

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('pedidos.db')
c = conn.cursor()

# Criação da tabela no banco de dados se não existir
c.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        hora TEXT,
        tipo_venda TEXT,
        codigo_cliente TEXT,
        tipo_produto TEXT,
        quantidade TEXT,
        endereco_entrega TEXT,
        telefone TEXT,
        ponto_referencia TEXT,
        latitude REAL,
        longitude REAL
    )
''')

# Função para inserir dados na tabela
def inserir_dados(tipo_venda, codigo_cliente, tipo_produto, quantidade, endereco_entrega, telefone, ponto_referencia, latitude, longitude):
    data = datetime.now().strftime('%Y-%m-%d')
    hora = datetime.now().strftime('%H:%M:%S')
    c.execute("INSERT INTO pedidos (data, hora, tipo_venda, codigo_cliente, tipo_produto, quantidade, endereco_entrega, telefone, ponto_referencia, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
              (data, hora, tipo_venda, codigo_cliente, tipo_produto, quantidade, endereco_entrega, telefone, ponto_referencia, latitude, longitude))
    conn.commit()

# Função para gerar o relatório PDF
def gerar_relatorio_pdf():
    c.execute("SELECT * FROM pedidos")
    dados_pedidos = c.fetchall()
    colunas = ["ID", "Data", "Hora", "Tipo de Venda", "Código do Cliente", "Tipo de Produto", "Quantidade", "Endereço de Entrega", "Telefone", "Ponto de Referência", "Latitude", "Longitude"]

    # Criar o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Adicionar título
    pdf.cell(200, 10, txt="Relatório de Pedidos", ln=True, align='C')
    pdf.ln(10)

    # Adicionar cabeçalhos das colunas
    pdf.set_font("Arial", size=10)
    for coluna in colunas:
        pdf.cell(30, 10, txt=coluna, border=1)
    pdf.ln()

    # Adicionar os dados dos pedidos
    for pedido in dados_pedidos:
        for item in pedido:
            pdf.cell(30, 10, txt=str(item), border=1)
        pdf.ln()

    # Salvar o PDF em um buffer
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return pdf_output

# Título da aplicação
st.title("Formulário de Entrega")

# Seleção do tipo (sem a opção "Venda Galpão")
tipo_venda = st.radio("Tipo", ["Venda Externa"])

# Código do cliente
codigo_cliente = st.text_input("Código do Cliente")

# Tipo de produto
tipo_produto = st.radio("Tipo produto", ["saco 20 kg", "amarrado 20 kg"])

# Quantidade
quantidade = st.text_input("Quantidade")

# Endereço de entrega
endereco_entrega = st.text_input("Endereço de Entrega")

# Telefone (campo obrigatório)
telefone = st.text_input("Telefone (obrigatório)")

# Ponto de referência
ponto_referencia = st.text_input("Ponto de Referência")

# Exibir o mapa para seleção da localização
st.header("Selecione a Localização para Entrega")
st.write("Clique no mapa para selecionar a localização onde deseja a entrega.")

# Adicionar o mapa com coordenadas de Maceió-AL
initial_location = [-9.6658, -35.7353]  # Coordenadas de Maceió-AL
location = st.map(pd.DataFrame({'lat': [initial_location[0]], 'lon': [initial_location[1]]}))

# Exibir os dados
if st.button("Enviar"):
    if telefone:
        latitude, longitude = obter_coordenadas(endereco_entrega)
        if latitude and longitude:
            st.write(f"Tipo de Venda: {tipo_venda}")
            st.write(f"Código do Cliente: {codigo_cliente}")
            st.write(f"Tipo de Produto: {tipo_produto}")
            st.write(f"Quantidade: {quantidade}")
            st.write(f"Endereço de Entrega: {endereco_entrega}")
            st.write(f"Telefone: {telefone}")
            st.write(f"Ponto de Referência: {ponto_referencia}")
            st.write(f"Latitude: {latitude}")
            st.write(f"Longitude: {longitude}")
            
            # Inserir dados no banco de dados
            inserir_dados(tipo_venda, codigo_cliente, tipo_produto, quantidade, endereco_entrega, telefone, ponto_referencia, latitude, longitude)
        else:
            st.write("Não foi possível obter as coordenadas do endereço.")
    else:
        st.error("O campo Telefone é obrigatório.")

# Exportar relatórios
st.header("Gerar Relatórios")

if st.button("Exportar Relatório em PDF"):
    pdf_output = gerar_relatorio_pdf()
    
    st.download_button(
        label="Baixar Relatório em PDF",
        data=pdf_output,
        file_name="relatorio_pedidos.pdf",
        mime="application/pdf"
    )

# Fechar a conexão com o banco de dados ao final
conn.close()
