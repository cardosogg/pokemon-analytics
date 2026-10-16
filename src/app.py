import streamlit as st
import pandas as pd
import sqlalchemy

# Configuração da página do Streamlit
st.set_page_config(page_title="Pokémon Analytics", page_icon="⚡", layout="wide")

# Ligação ao PostgreSQL (a mesma que validámos no pipeline)
DB_USER = "airflow"
DB_PASSWORD = "airflow"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "airflow"

@st.cache_data
def load_data():
    engine = sqlalchemy.create_engine(f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    query = "SELECT * FROM pokemon_stats"
    return pd.read_sql(query, engine)

# Título principal
st.title("⚡ Pokémon Analytics Dashboard")
st.markdown("Visualização interativa dos dados extraídos da PokéAPI através do nosso pipeline ETL.")

# Carregar os dados
try:
    df = load_data()
    
    # Métricas de topo (KPIs)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Pokémon", len(df))
    col2.metric("Ataque Médio", f"{df['attack'].mean():.1f}")
    col3.metric("Defesa Média", f"{df['defense'].mean():.1f}")
    col4.metric("Velocidade Média", f"{df['speed'].mean():.1f}")

    st.divider()

    # Filtros interativos na barra lateral (usando primary_type)
    st.sidebar.header("🔍 Filtros")
    selected_type = st.sidebar.selectbox("Filtrar por Tipo Principal:", options=["Todos"] + sorted(df['primary_type'].unique().tolist()))

    if selected_type != "Todos":
        filtered_df = df[df['primary_type'] == selected_type]
    else:
        filtered_df = df

    # Layout com duas colunas
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader(f"📋 Lista de Pokémon ({len(filtered_df)})")
        st.dataframe(filtered_df[['pokemon_name', 'primary_type', 'hp', 'attack', 'defense', 'speed']], height=400)

    with col_right:
        st.subheader("⚔️ Comparativo de Ataque")
        # Gráfico de barras simples com o Streamlit (usando pokemon_name)
        chart_data = filtered_df.set_index('pokemon_name')['attack']
        st.bar_chart(chart_data, height=400)

except Exception as e:
    st.error(f"Erro ao ligar à base de dados ou carregar dados: {e}")