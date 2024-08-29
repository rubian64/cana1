import streamlit as st
import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import numpy as np
from datetime import datetime

# Função para conectar ao banco de dados SQLite e criar a tabela se não existir
def connect_to_db_and_create_table(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Criar a tabela fluxo_de_caixa se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fluxo_de_caixa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Data DATE,
                Entradas FLOAT,
                Saídas FLOAT,
                Saldo FLOAT
            );
        ''')
        
        # Verificar se a tabela já possui dados
        cursor.execute("SELECT COUNT(*) FROM fluxo_de_caixa")
        count = cursor.fetchone()[0]
        
        # Popular a tabela com 1000 dados aleatórios se estiver vazia
        if count == 0:
            random_dates = pd.date_range(start='2023-01-01', end='2026-12-31', periods=1000)
            entradas = np.random.uniform(low=100, high=1000, size=1000)
            saídas = np.random.uniform(low=50, high=500, size=1000)
            saldo = np.cumsum(entradas - saídas)
            
            data_to_insert = [(date.strftime('%Y-%m-%d'), entrada, saída, saldo) for date, entrada, saída, saldo in zip(random_dates, entradas, saídas, saldo)]
            
            cursor.executemany('''
                INSERT INTO fluxo_de_caixa (Data, Entradas, Saídas, Saldo) 
                VALUES (?, ?, ?, ?);
            ''', data_to_insert)
            
            conn.commit()
            st.success("Tabela fluxo_de_caixa criada e populada com sucesso!")
        
        return conn
    except sqlite3.Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para obter os dados financeiros do banco de dados
def get_financial_data(conn):
    try:
        query = "SELECT * FROM fluxo_de_caixa;"
        df = pd.read_sql(query, conn)
        return df
    except sqlite3.Error as e:
        st.error(f"Erro ao obter dados financeiros: {e}")
        return pd.DataFrame()

# Lista de bancos de dados SQLite
databases = ["usuarios.db", "motoristas.db", "clientes.db", "vendas2.db"]

# Título do aplicativo Streamlit
st.title("Relatório de Fluxo de Caixa - Gestão Financeira")

# Selecionar um banco de dados
selected_db = st.selectbox("Escolha um banco de dados para visualizar", databases)

# Conectar ao banco de dados selecionado e criar a tabela se necessário
conn = connect_to_db_and_create_table(selected_db)

# Verificar se a conexão foi bem sucedida
if conn is not None:
    # Obter os dados financeiros do banco de dados
    df = get_financial_data(conn)
    
    # Fechar a conexão com o banco de dados
    conn.close()
else:
    st.error("Falha ao conectar ao banco de dados.")

# Verificar se há dados para análise
if not df.empty:
    st.subheader("Dados Financeiros")
    st.write(df.head())  # Mostrar apenas os primeiros registros para visualização inicial

    # Gerar gráficos de análise financeira
    st.subheader("Análise de Fluxo de Caixa")
    
    # Gráfico de linha para visualizar o fluxo de caixa ao longo do tempo
    plt.figure(figsize=(10, 6))
    plt.plot(df['Data'], df['Saldo'], marker='o', linestyle='-', color='b')
    plt.title('Fluxo de Caixa ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Saldo (R$)')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Insights sobre os dados financeiros
    total_entradas = df['Entradas'].sum()
    total_saidas = df['Saídas'].sum()
    saldo_atual = df['Saldo'].iloc[-1]

    st.subheader("Insights Financeiros")
    st.write("Total de Entradas:", total_entradas)
    st.write("Total de Saídas:", total_saidas)
    st.write("Saldo Atual:", saldo_atual)

else:
    st.warning("Nenhum dado financeiro encontrado.")

# Modelagem preditiva com Regressão Linear
future_predictions = []
if not df.empty and len(df) > 5:
    st.subheader("Modelagem Preditiva com Regressão Linear")

    # Preparar os dados para a regressão linear
    X = df.index.values.reshape(-1, 1)  # Usaremos os índices como variável independente
    y = df['Entradas'].values           # Variável dependente: Entradas

    # Criar o modelo de regressão linear
    model = LinearRegression()
    model.fit(X, y)

    # Prever os próximos 5 valores de faturamento
    next_periods = 5
    future_indices = pd.Series(range(len(df), len(df) + next_periods))
    future_predictions = model.predict(future_indices.values.reshape(-1, 1))

    st.write("Próximos Faturamentos Previstos:")
    for i in range(next_periods):
        st.write(f"Próximo período {i+1}: R$ {future_predictions[i]:.2f}")

else:
    st.warning("Não há dados suficientes para realizar a modelagem preditiva.")

# Gerar relatório em PDF usando ReportLab
if not df.empty:
    st.subheader("Relatório em PDF")

    # Função para gerar o PDF
    def generate_pdf():
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Título do relatório
        c.setFont("Helvetica-Bold", 18)
        c.drawString(100, 750, "Relatório de Fluxo de Caixa - Gestão Financeira")

        # Data e Hora
        c.setFont("Helvetica", 12)
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        c.drawString(100, 730, f"Data e Hora do Relatório: {now}")
        
        # Dados financeiros
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 700, "Dados Financeiros")
        c.setFont("Helvetica", 12)
        c.drawString(100, 680, f"Total de Entradas: R$ {total_entradas:.2f}")
        c.drawString(100, 660, f"Total de Saídas: R$ {total_saidas:.2f}")
        c.drawString(100, 640, f"Saldo Atual: R$ {saldo_atual:.2f}")
        
        # Gráfico de Fluxo de Caixa
        plt.figure(figsize=(6, 4))
        plt.plot(df['Data'], df['Saldo'], marker='o', linestyle='-', color='b')
        plt.title('Fluxo de Caixa ao Longo do Tempo')
        plt.xlabel('Data')
        plt.ylabel('Saldo (R$)')
        plt.xticks(rotation=45)
        
        imgdata = BytesIO()
        plt.savefig(imgdata, format='png')
        imgdata.seek(0)
        c.drawImage(ImageReader(imgdata), 100, 400, width=400, height=300)
        
        plt.close()  # Fechar o gráfico para liberar a memória

        # Insights financeiros
        c.drawString(100, 380, "Insights Financeiros")
        c.drawString(100, 360, f"Total de Entradas: R$ {total_entradas:.2f}")
        c.drawString(100, 340, f"Total de Saídas: R$ {total_saidas:.2f}")
        c.drawString(100, 320, f"Saldo Atual: R$ {saldo_atual:.2f}")

        # Modelagem preditiva
        if len(future_predictions) > 0:
            c.drawString(100, 300, "Modelagem Preditiva com Regressão Linear")
            for i in range(next_periods):
                c.drawString(100, 280 - i*20, f"Próximo período {i+1}: R$ {future_predictions[i]:.2f}")

        c.showPage()
        c.save()
        
        buffer.seek(0)
        return buffer

    # Gerar o PDF e disponibilizar o link para download
    pdf = generate_pdf()
    st.download_button(label="Baixar Relatório em PDF", data=pdf, file_name="relatorio_fluxo_de_caixa.pdf", mime="application/pdf")

else:
    st.warning("Não há dados suficientes para gerar o relatório em PDF.")
