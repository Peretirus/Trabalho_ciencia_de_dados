import streamlit as st
import pandas as pd
import plotly.express as px

# Título do Dashboard
st.set_page_config(page_title='Dashboard de Preços de Casas', layout='wide')
st.title('🏡 Dashboard Interativo - Análise de Preços de Imóveis (Ames Housing)')

# Carregar dados
@st.cache_data
def carregar_dados():
    return pd.read_csv('train.csv')

df = carregar_dados()

# Filtro por Bairro
st.sidebar.header('Filtros')
bairros = df['Neighborhood'].unique()
bairro_escolhido = st.sidebar.selectbox('Selecione um Bairro:', sorted(bairros))

df_bairro = df[df['Neighborhood'] == bairro_escolhido]

# 1. Distribuição de Preço de Venda no Bairro Selecionado
st.subheader(f'Distribuição dos Preços em: {bairro_escolhido}')
fig1 = px.histogram(df_bairro, x='SalePrice', nbins=30, title='Distribuição dos Preços de Venda')
st.plotly_chart(fig1, use_container_width=True)

# 2. Relação entre Área Construída e Preço
st.subheader('Área Construída x Preço de Venda')
fig2 = px.scatter(df, x='GrLivArea', y='SalePrice', color='OverallQual',
                  hover_data=['Neighborhood'],
                  title='Casas maiores tendem a valer mais (colorido por Qualidade)')
st.plotly_chart(fig2, use_container_width=True)

# 3. Boxplot por Qualidade Geral
st.subheader('Preço por Qualidade Geral da Casa')
fig3 = px.box(df, x='OverallQual', y='SalePrice', title='Relação entre Qualidade e Preço')
st.plotly_chart(fig3, use_container_width=True)

# 4. Preço Médio por Bairro (Top 10)
st.subheader('Top 10 Bairros com Maior Preço Médio')
top_bairros = df.groupby('Neighborhood')['SalePrice'].mean().sort_values(ascending=False).head(10)
fig4 = px.bar(x=top_bairros.values, y=top_bairros.index,
              orientation='h', title='Bairros Mais Valorizados')
st.plotly_chart(fig4, use_container_width=True)

# 5. Preço médio por ano de construção
st.subheader('Preço Médio por Ano de Construção')
preco_ano = df.groupby('YearBuilt')['SalePrice'].mean()
fig5 = px.line(x=preco_ano.index, y=preco_ano.values,
               labels={'x': 'Ano de Construção', 'y': 'Preço Médio'},
               title='Tendência Histórica do Preço')
st.plotly_chart(fig5, use_container_width=True)
