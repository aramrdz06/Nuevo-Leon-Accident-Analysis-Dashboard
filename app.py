import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import numpy as np

# ---------------------------
# CONFIGURACIÓN
# ---------------------------
st.set_page_config(page_title="Dashboard Accidentes NL", layout="wide")

st.title("📊 Sistema de Monitoreo de Accidentes - Nuevo León")
st.markdown("Análisis de Big Data para la toma de decisiones en el Sector Transporte/Gobierno.")

# ---------------------------
# 1. CARGA Y LIMPIEZA
# ---------------------------
@st.cache_data
def load_data():
    # ✅ Ruta correcta (archivo en la misma carpeta)
    df = pd.read_csv('sct_71_accidentes_mes.csv', encoding='latin-1')

    df['entidad_federativa'] = df['entidad_federativa'].str.strip()

    df_nl = df[df['entidad_federativa'].str.contains('Nuevo', case=False, na=False)].copy()

    meses_ordenados = [
        'enero','febrero','marzo','abril','mayo','junio',
        'julio','agosto','septiembre','octubre','noviembre','diciembre'
    ]

    df_nl['mes'] = pd.Categorical(
        df_nl['mes'],
        categories=meses_ordenados,
        ordered=True
    )

    return df_nl.sort_values('mes')

df_nl = load_data()

st.write("Filas encontradas:", len(df_nl))

# ---------------------------
# 2. FILTROS
# ---------------------------
st.sidebar.header("Filtros del Tablero")

mes_seleccionado = st.sidebar.multiselect(
    "Selecciona meses:",
    options=df_nl['mes'].unique().tolist(),
    default=df_nl['mes'].unique().tolist()
)

df_filtrado = df_nl[df_nl['mes'].isin(mes_seleccionado)]

# ---------------------------
# 3. VISUALIZACIONES
# ---------------------------
col1, col2 = st.columns(2)

# 📍 MAPA
with col1:
    st.subheader("📍 Visualización Geoespacial")

    m = folium.Map(location=[25.6866, -100.3161], zoom_start=7)

    total = df_filtrado["accidentes"].sum()

    folium.Circle(
        location=[25.6866, -100.3161],
        radius=max(total * 200, 10000),
        popup=f"Total accidentes: {total}",
        color="red",
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

    st_folium(m, width=500, height=400)

# 🔥 HEATMAP
with col2:
    st.subheader("🔥 Heatmap de Densidad")

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

# 🫧 BUBBLE
st.subheader("🫧 Gráfico de Burbujas")

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

# ===========================
# ⭐ MONITOREO EN TIEMPO REAL
# ===========================
st.divider()
st.subheader("⏱️ Monitoreo en Tiempo Real")

valor = np.random.randint(50, 200)

st.metric("🚗 Accidentes registrados ahora", valor)

datos_rt = pd.DataFrame({
    "tiempo": range(20),
    "accidentes": np.random.randint(0, 100, 20)
})

fig_rt = px.line(datos_rt, x="tiempo", y="accidentes")
st.plotly_chart(fig_rt, use_container_width=True)

st.caption("🔄 Actualiza la página para simular nuevos datos")