import streamlit as st
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from fpdf import FPDF
import os

# Configuração inicial do Streamlit
st.title("Sistema de Gestão Financeira - DRE")

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('dados_financeiros.db')
c = conn.cursor()

# Criação da tabela no banco de dados se não existir
c.execute('''
    CREATE TABLE IF NOT EXISTS dre (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        categoria TEXT,
        tipo TEXT,
        valor REAL
    )
''')

# Função para inserir dados na tabela
def inserir_dados(categoria, tipo, valor):
    data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO dre (data, categoria, tipo, valor) VALUES (?, ?, ?, ?)", 
              (data, categoria, tipo, valor))
    conn.commit()

# Interface de entrada de dados
st.header("Entrada de Dados")

# Seleção de categoria
categoria = st.selectbox("Selecione a categoria", [
    "Receita de Vendas",
    "Impostos",
    "Despesas de Vendas",
    "Despesas Operacionais",
    "Receitas/Despesas Diversas"
])

# Seleção de tipo
if categoria == "Receita de Vendas":
    tipo = st.selectbox("Tipo de Receita", ["Venda de Produto", "Venda de Serviço"])
elif categoria == "Impostos":
    tipo = st.selectbox("Tipo de Imposto", ["IPI", "ICMS", "ISSQN", "Outros Impostos"])
elif categoria == "Despesas de Vendas":
    tipo = st.selectbox("Tipo de Despesa de Vendas", ["Comissão", "Embalagens", "Frete", "Outras Despesas"])
elif categoria == "Despesas Operacionais":
    tipo = st.selectbox("Tipo de Despesa Operacional", [
       "Juros bancários","Tarifas bancárias","Gasolina","Água", "Aluguel", "Condomínio", "FGTS", "INSS", 
        "Luz", "Internet", "Material de Escritório", "Material de Consumo", "Salário", "Outras Despesas"])
else:
    tipo = st.selectbox("Tipo de Receita/Despesa Diversa", [
        "Rendimento Financeiro", "Outras Receitas", 
        "Tarifas Bancárias", "Juros e Multas", "Outras Despesas"])

valor = st.number_input("Informe o valor", min_value=0.0, format="%.2f")

if st.button("Salvar"):
    if valor > 0:
        inserir_dados(categoria, tipo, valor)
        st.success(f"{categoria} ({tipo}) de R${valor:.2f} salva com sucesso!")
    else:
        st.error("Por favor, insira um valor válido.")

# Função para calcular totais
def calcular_totais():
    # Receita de Vendas
    c.execute("SELECT SUM(valor) FROM dre WHERE categoria = 'Receita de Vendas'")
    receita_vendas = c.fetchone()[0] or 0.0
    
    # Impostos
    c.execute("SELECT SUM(valor) FROM dre WHERE categoria = 'Impostos'")
    impostos = c.fetchone()[0] or 0.0
    
    receita_liquida = receita_vendas - impostos
    
    # Despesas de Vendas
    c.execute("SELECT SUM(valor) FROM dre WHERE categoria = 'Despesas de Vendas'")
    despesas_vendas = c.fetchone()[0] or 0.0
    
    lucro_bruto = receita_liquida - despesas_vendas
    
    # Despesas Operacionais
    c.execute("SELECT SUM(valor) FROM dre WHERE categoria = 'Despesas Operacionais'")
    despesas_operacionais = c.fetchone()[0] or 0.0
    
    lucro_operacional = lucro_bruto - despesas_operacionais
    
    # Receitas/Despesas Diversas
    c.execute("SELECT SUM(valor) FROM dre WHERE categoria = 'Receitas/Despesas Diversas'")
    receitas_despesas_diversas = c.fetchone()[0] or 0.0
    
    lucro_prejuizo = lucro_operacional + receitas_despesas_diversas
    
    return receita_vendas, impostos, receita_liquida, despesas_vendas, lucro_bruto, despesas_operacionais, lucro_operacional, receitas_despesas_diversas, lucro_prejuizo

# Exibição de dados e saldo
st.header("DRE Resumida")
receita_vendas, impostos, receita_liquida, despesas_vendas, lucro_bruto, despesas_operacionais, lucro_operacional, receitas_despesas_diversas, lucro_prejuizo = calcular_totais()

st.metric("Receita de Vendas", f"R${receita_vendas:.2f}")
st.metric("Impostos", f"R${impostos:.2f}")
st.metric("Receita Líquida", f"R${receita_liquida:.2f}")
st.metric("Lucro Bruto", f"R${lucro_bruto:.2f}")
st.metric("Despesas Operacionais", f"R${despesas_operacionais:.2f}")
st.metric("Lucro Operacional", f"R${lucro_operacional:.2f}")
st.metric("Lucro/Prejuízo", f"R${lucro_prejuizo:.2f}")

# Gráfico de Barras: Receitas vs Despesas
st.header("Gráfico de Barras: Receitas vs Despesas")
fig, ax = plt.subplots()
ax.bar(['Receita Líquida', 'Despesas Operacionais'], [receita_liquida, despesas_operacionais], color=['green', 'red'])
ax.set_ylabel('Valor em R$')
ax.set_title('Receita Líquida vs Despesas Operacionais')
st.pyplot(fig)

# Gráfico de Pizza: Distribuição das Despesas Operacionais
st.header("Gráfico de Pizza: Distribuição das Despesas Operacionais")
despesas_op = []
tipos_despesas_op = []

for tipo_op in ["Juros bancários","Tarifas bancárias","Gasolina","Água", "Aluguel", "Condomínio", "FGTS", "INSS", "Luz", "Internet", "Material de Escritório", "Material de Consumo", "Salário", "Outras Despesas"]:
    c.execute(f"SELECT SUM(valor) FROM dre WHERE categoria = 'Despesas Operacionais' AND tipo = '{tipo_op}'")
    valor_op = c.fetchone()[0] or 0.0
    if valor_op > 0:
        despesas_op.append(valor_op)
        tipos_despesas_op.append(tipo_op)

fig, ax = plt.subplots()
ax.pie(despesas_op, labels=tipos_despesas_op, autopct='%1.1f%%')
ax.set_title('Distribuição das Despesas Operacionais')
st.pyplot(fig)

# Gráfico de Linhas: Lucro Operacional ao longo do tempo
st.header("Gráfico de Linhas: Lucro Operacional ao Longo do Tempo")
c.execute("SELECT data, SUM(valor) FROM dre WHERE categoria = 'Despesas Operacionais' OR categoria = 'Receita de Vendas' GROUP BY data")
dados = c.fetchall()

datas = [datetime.strptime(d[0], '%Y-%m-%d %H:%M:%S') for d in dados]
valores = [d[1] for d in dados]

fig, ax = plt.subplots()
ax.plot(datas, valores, marker='o')
ax.set_xlabel('Data')
ax.set_ylabel('Lucro Operacional em R$')
ax.set_title('Lucro Operacional ao Longo do Tempo')
ax.grid(True)
st.pyplot(fig)

# Exportar DRE para CSV
st.header("Exportar DRE")

c.execute("SELECT * FROM dre")
dados_dre = c.fetchall()
colunas = ["ID", "Data", "Categoria", "Tipo", "Valor"]

df_dre = pd.DataFrame(dados_dre, columns=colunas)

# Botão para exportar CSV
st.download_button(label="Exportar DRE para CSV", data=df_dre.to_csv(index=False), file_name="dre.csv", mime="text/csv")

# Função para gerar PDF
def gerar_pdf():
    # Gerar e salvar os gráficos como imagens
    fig1, ax1 = plt.subplots()
    ax1.bar(['Receita Líquida', 'Despesas Operacionais'], [receita_liquida, despesas_operacionais], color=['green', 'red'])
    ax1.set_ylabel('Valor em R$')
    ax1.set_title('Receita Líquida vs Despesas Operacionais')
    fig1.savefig('grafico_barras.png')

    fig2, ax2 = plt.subplots()
    ax2.pie(despesas_op, labels=tipos_despesas_op, autopct='%1.1f%%')
    ax2.set_title('Distribuição das Despesas Operacionais')
    fig2.savefig('grafico_pizza.png')

    fig3, ax3 = plt.subplots()
    ax3.plot(datas, valores, marker='o')
    ax3.set_xlabel('Data')
    ax3.set_ylabel('Lucro Operacional em R$')
    ax3.set_title('Lucro Operacional ao Longo do Tempo')
    ax3.grid(True)
    fig3.savefig('grafico_linhas.png')

    # Criar o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Demonstração do Resultado do Exercício (DRE)", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=10)
    for i, row in df_dre.iterrows():
        pdf.cell(200, 10, txt=f"{row['Data']} - {row['Categoria']} - {row['Tipo']} - R${row['Valor']:.2f}", ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, txt="Gráficos", ln=True, align='C')
    pdf.ln(10)
    
    # Adicionar os gráficos ao PDF
    pdf.image('grafico_barras.png', x=10, y=None, w=180)
    pdf.ln(85)  # Ajustar o espaçamento
    pdf.image('grafico_pizza.png', x=10, y=None, w=180)
    pdf.ln(85)
    pdf.image('grafico_linhas.png', x=10, y=None, w=180)

    # Salvar o PDF
    pdf_path = "dre.pdf"
    pdf.output(pdf_path)
    return pdf_path

# Adicionar botão para gerar PDF
if st.button("Gerar PDF"):
    pdf_path = gerar_pdf()
    with open(pdf_path, "rb") as f:
        st.download_button(label="Baixar DRE em PDF", data=f, file_name="dre.pdf", mime="application/pdf")
    os.remove(pdf_path)  # Remover o arquivo PDF após o download

# Fechar a conexão com o banco de dados ao final
conn.close()
