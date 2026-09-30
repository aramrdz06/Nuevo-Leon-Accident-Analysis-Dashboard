import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# CONFIGURACIÓN
st.set_page_config(page_title="Dashboard Accidentes NL", layout="wide")

st.title("Dashboard de Accidentes - Nuevo León")
st.markdown(
    "Análisis de accidentes por entidad federativa y mes. "
    "Fuente: archivo `sct_71_accidentes_mes.csv` (SCT)."
)

MESES = [
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
]


# 1. CARGA Y LIMPIEZA
@st.cache_data
def load_data():
    df = pd.read_csv('sct_71_accidentes_mes.csv', encoding='latin-1')
    df['entidad_federativa'] = df['entidad_federativa'].str.strip()
    df['mes'] = pd.Categorical(df['mes'], categories=MESES, ordered=True)
    return df.sort_values('mes')


df_all = load_data()
df_nl = df_all[df_all['entidad_federativa'].str.contains('Nuevo', case=False, na=False)].copy()

# ---------------------------
# 2. FILTROS
# ---------------------------
st.sidebar.header("Filtros del Tablero")

meses_disponibles = [m for m in MESES if m in df_nl['mes'].unique().tolist()]
mes_seleccionado = st.sidebar.multiselect(
    "Selecciona meses:",
    options=meses_disponibles,
    default=meses_disponibles
)

df_filtrado = df_nl[df_nl['mes'].isin(mes_seleccionado)]

# Resumen rápido
c1, c2, c3, c4 = st.columns(4)
c1.metric("Accidentes", int(df_filtrado["accidentes"].sum()))
c2.metric("Heridos", int(df_filtrado["heridos"].sum()))
c3.metric("Muertos", int(df_filtrado["muertos"].sum()))
c4.metric("Daños materiales (millones)", round(df_filtrado["danios_materiales_millones"].sum(), 2))

st.divider()

# ---------------------------
# 3. VISUALIZACIONES
# ---------------------------
col1, col2 = st.columns(2)

# MAPA
with col1:
    st.subheader("Mapa: total de accidentes en Nuevo León")
    m = folium.Map(location=[25.6866, -100.3161], zoom_start=7)

    total = df_filtrado["accidentes"].sum()

    folium.Circle(
        location=[25.6866, -100.3161],
        radius=max(total * 200, 10000),
        popup=f"Total accidentes: {int(total)}",
        color="red",
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

    st_folium(m, width=500, height=400)

# HEATMAP
with col2:
    st.subheader("Heatmap: accidentes y heridos por mes")
    if len(df_filtrado) > 0:
        fig_heat = px.density_heatmap(
            df_filtrado,
            x="mes",
            y="accidentes",
            z="heridos",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig_heat, use_container_width=True)

st.divider()

# BURBUJAS
st.subheader("Heridos vs. daños materiales (tamaño = muertos)")
if len(df_filtrado) > 0:
    fig_bubble = px.scatter(
        df_filtrado,
        x="heridos",
        y="danios_materiales_millones",
        size="muertos",
        color="mes",
        size_max=50
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

# COMPARACIÓN ENTRE ESTADOS (datos reales del mismo archivo)
st.divider()
st.subheader("Nuevo León frente a otros estados")
df_estados = df_all[df_all['mes'].isin(mes_seleccionado)]
if len(df_estados) > 0:
    top = (
        df_estados.groupby('entidad_federativa', observed=True)['accidentes']
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    top['Estado'] = top['entidad_federativa'].apply(
        lambda e: 'Nuevo León' if 'Nuevo' in e else 'Otros'
    )
    fig_top = px.bar(
        top,
        x="accidentes",
        y="entidad_federativa",
        color="Estado",
        orientation="h",
        color_discrete_map={'Nuevo León': '#d62728', 'Otros': '#9aa0a6'},
        labels={"entidad_federativa": "Entidad", "accidentes": "Accidentes"},
        title="Top 10 entidades por número de accidentes (meses seleccionados)"
    )
    fig_top.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_top, use_container_width=True)
    st.caption("Si Nuevo León no aparece en el top 10 con los meses elegidos, no se muestra en la gráfica.")