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

def connect_to_db(db_name):
    try:
        return sqlite3.connect(db_name)
    except sqlite3.Error as e:
        st.error(f"Erro ao conectar ao banco de dados {db_name}: {e}")
        return None

def update_fluxo_de_caixa():
    # Conectar aos bancos de dados
    conn_usuarios = connect_to_db('usuarios.db')
    conn_motoristas = connect_to_db('motoristas.db')
    conn_clientes = connect_to_db('clientes.db')
    conn_vendas = connect_to_db('vendas2.db')
    
    # Consultas para obter dados relevantes
    vendas_query = """
        SELECT 
            Data,
            SUM(Valor) AS Entradas
        FROM vendas
        GROUP BY Data;
    """
    
    pagamentos_query = """
        SELECT 
            Data,
            SUM(Valor) AS Saídas
        FROM pagamentos
        GROUP BY Data;
    """
    
    vendas_df = pd.read_sql_query(vendas_query, conn_vendas)
    pagamentos_df = pd.read_sql_query(pagamentos_query, conn_vendas)
    
    conn_usuarios.close()
    conn_motoristas.close()
    conn_clientes.close()
    conn_vendas.close()
    
    fluxo_df = pd.merge(vendas_df, pagamentos_df, on='Data', how='outer')
    fluxo_df.fillna(0, inplace=True)
    fluxo_df['Saldo'] = fluxo_df['Entradas'] - fluxo_df['Saídas']
    fluxo_df['Saldo'] = fluxo_df['Saldo'].cumsum()
    
    conn_fluxo = connect_to_db('fluxo_de_caixa.db')
    if conn_fluxo:
        cursor = conn_fluxo.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fluxo_de_caixa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Data DATE,
                Entradas FLOAT,
                Saídas FLOAT,
                Saldo FLOAT
            );
        ''')
        cursor.execute('DELETE FROM fluxo_de_caixa')
        
        for _, row in fluxo_df.iterrows():
            cursor.execute('''
                INSERT INTO fluxo_de_caixa (Data, Entradas, Saídas, Saldo) 
                VALUES (?, ?, ?, ?);
            ''', (row['Data'], row['Entradas'], row['Saídas'], row['Saldo']))
        
        conn_fluxo.commit()
        conn_fluxo.close()
    else:
        st.error("Não foi possível conectar ao banco de dados de fluxo de caixa.")

def get_financial_data():
    try:
        conn = connect_to_db('fluxo_de_caixa.db')
        if conn:
            query = "SELECT * FROM fluxo_de_caixa;"
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        else:
            return pd.DataFrame()
    except sqlite3.Error as e:
        st.error(f"Erro ao obter dados financeiros: {e}")
        return pd.DataFrame()

st.title("Relatório de Fluxo de Caixa - Gestão Financeira")

update_fluxo_de_caixa()
df = get_financial_data()

if not df.empty:
    st.subheader("Dados Financeiros")
    st.write(df.head())
    
    st.subheader("Análise de Fluxo de Caixa")
    plt.figure(figsize=(10, 6))
    plt.plot(df['Data'], df['Saldo'], marker='o', linestyle='-', color='b')
    plt.title('Fluxo de Caixa ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Saldo (R$)')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    total_entradas = df['Entradas'].sum()
    total_saidas = df['Saídas'].sum()
    saldo_atual = df['Saldo'].iloc[-1]

    st.subheader("Insights Financeiros")
    st.write(f"Total de Entradas: R$ {total_entradas:.2f}")
    st.write(f"Total de Saídas: R$ {total_saidas:.2f}")
    st.write(f"Saldo Atual: R$ {saldo_atual:.2f}")

    future_predictions = []
    if len(df) > 5:
        st.subheader("Modelagem Preditiva com Regressão Linear")

        X = df.index.values.reshape(-1, 1)
        y = df['Entradas'].values

        model = LinearRegression()
        model.fit(X, y)

        next_periods = 5
        future_indices = pd.Series(range(len(df), len(df) + next_periods))
        future_predictions = model.predict(future_indices.values.reshape(-1, 1))

        st.write("Próximos Faturamentos Previstos:")
        for i in range(next_periods):
            st.write(f"Próximo período {i+1}: R$ {future_predictions[i]:.2f}")

    st.subheader("Relatório em PDF")

    def generate_pdf():
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        c.setFont("Helvetica-Bold", 18)
        c.drawString(100, 750, "Relatório de Fluxo de Caixa - Gestão Financeira")
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        c.setFont("Helvetica", 12)
        c.drawString(100, 730, f"Data e Hora do Relatório: {now}")
        
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 700, "Dados Financeiros")
        c.setFont("Helvetica", 12)
        c.drawString(100, 680, f"Total de Entradas: R$ {total_entradas:.2f}")
        c.drawString(100, 660, f"Total de Saídas: R$ {total_saidas:.2f}")
        c.drawString(100, 640, f"Saldo Atual: R$ {saldo_atual:.2f}")
        
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
        
        plt.close()

        c.drawString(100, 380, "Insights Financeiros")
        c.drawString(100, 360, f"Total de Entradas: R$ {total_entradas:.2f}")
        c.drawString(100, 340, f"Total de Saídas: R$ {total_saidas:.2f}")
        c.drawString(100, 320, f"Saldo Atual: R$ {saldo_atual:.2f}")

        if len(future_predictions) > 0:
            c.drawString(100, 300, "Modelagem Preditiva com Regressão Linear")
            for i in range(next_periods):
                c.drawString(100, 280 - i*20, f"Próximo período {i+1}: R$ {future_predictions[i]:.2f}")

        c.showPage()
        c.save()
        
        buffer.seek(0)
        return buffer

    pdf = generate_pdf()
    st.download_button(label="Baixar Relatório em PDF", data=pdf, file_name="relatorio_fluxo_de_caixa.pdf", mime="application/pdf")

else:
    st.warning("Não há dados suficientes para gerar o relatório em PDF.")
