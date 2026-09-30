import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# CONFIGURACIÓN
st.set_page_config(page_title="Dashboard de Accidentes", layout="wide")

MESES = [
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
]

# Punto de referencia en el mapa: capital de cada estado (aprox.).
# El dataset no trae ubicación exacta de los accidentes.
CAPITALES = {
    'Aguascalientes': (21.8853, -102.2916),
    'Baja California': (32.6245, -115.4523),
    'Baja California Sur': (24.1426, -110.3128),
    'Campeche': (19.8301, -90.5349),
    'Chiapas': (16.7528, -93.1152),
    'Chihuahua': (28.6353, -106.0889),
    'Ciudad De Mexico': (19.4326, -99.1332),
    'Coahuila': (25.4232, -101.0053),
    'Colima': (19.2433, -103.7250),
    'Durango': (24.0277, -104.6532),
    'Estado Mexico': (19.2826, -99.6557),
    'Guanajuato': (21.0190, -101.2574),
    'Guerrero': (17.5506, -99.5058),
    'Hidalgo': (20.1011, -98.7591),
    'Jalisco': (20.6597, -103.3496),
    'Michoacan': (19.7060, -101.1950),
    'Morelos': (18.9242, -99.2216),
    'Nayarit': (21.5058, -104.8946),
    'Nuevo Leon': (25.6866, -100.3161),
    'Oaxaca': (17.0732, -96.7266),
    'Puebla': (19.0414, -98.2063),
    'Queretaro': (20.5888, -100.3899),
    'Quintana Roo': (18.5001, -88.2960),
    'San Luis Potosi': (22.1565, -100.9855),
    'Sinaloa': (24.8091, -107.3940),
    'Sonora': (29.0729, -110.9559),
    'Tabasco': (17.9892, -92.9475),
    'Tamaulipas': (23.7369, -99.1411),
    'Tlaxcala': (19.3139, -98.2404),
    'Veracruz': (19.5438, -96.9102),
    'Yucatan': (20.9674, -89.5926),
    'Zacatecas': (22.7709, -102.5832),
}
CENTRO_MEXICO = (23.6345, -102.5528)

METRICAS = {
    "Accidentes": "accidentes",
    "Heridos": "heridos",
    "Muertos": "muertos",
    "Muertos por cada 100 accidentes": "muertos_x100",
}


# 1. CARGA Y LIMPIEZA
@st.cache_data
def load_data():
    df = pd.read_csv('sct_71_accidentes_mes.csv', encoding='latin-1')
    df['entidad_federativa'] = df['entidad_federativa'].str.strip()
    df['mes'] = pd.Categorical(df['mes'], categories=MESES, ordered=True)
    return df.sort_values('mes')


def muertos_por_100(muertos, accidentes):
    return round(muertos / accidentes * 100, 1) if accidentes > 0 else 0.0


df_all = load_data()

# ---------------------------
# 2. FILTROS
# ---------------------------
st.sidebar.header("Filtros del Tablero")

estados = sorted(df_all['entidad_federativa'].unique().tolist())
indice_nl = estados.index('Nuevo Leon') if 'Nuevo Leon' in estados else 0
estado = st.sidebar.selectbox("Selecciona un estado:", estados, index=indice_nl)

df_estado = df_all[df_all['entidad_federativa'] == estado]

meses_disponibles = [m for m in MESES if m in df_estado['mes'].unique().tolist()]
mes_seleccionado = st.sidebar.multiselect(
    "Selecciona meses:",
    options=meses_disponibles,
    default=meses_disponibles
)

df_filtrado = df_estado[df_estado['mes'].isin(mes_seleccionado)]

# ---------------------------
# 3. ENCABEZADO Y RESUMEN
# ---------------------------
st.title(f"Dashboard de Accidentes - {estado}")
st.markdown(
    "Análisis de accidentes por entidad federativa y mes. "
    "Fuente: archivo `sct_71_accidentes_mes.csv` (SCT)."
)

tot_acc = df_filtrado["accidentes"].sum()
tot_her = df_filtrado["heridos"].sum()
tot_mue = df_filtrado["muertos"].sum()
tot_dan = df_filtrado["danios_materiales_millones"].sum()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Accidentes", int(tot_acc))
c2.metric("Heridos", int(tot_her))
c3.metric("Muertos", int(tot_mue))
c4.metric("Daños materiales (millones)", round(tot_dan, 2))
c5.metric("Muertos por cada 100 accidentes", muertos_por_100(tot_mue, tot_acc))

st.divider()

# ---------------------------
# 4. VISUALIZACIONES
# ---------------------------
col1, col2 = st.columns(2)

# MAPA
with col1:
    st.subheader(f"Mapa: total de accidentes en {estado}")
    lat, lon = CAPITALES.get(estado, CENTRO_MEXICO)
    m = folium.Map(location=[lat, lon], zoom_start=7)

    folium.Circle(
        location=[lat, lon],
        radius=max(tot_acc * 200, 10000),
        popup=f"Total accidentes: {int(tot_acc)}",
        color="red",
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

    st_folium(m, width=500, height=400)
    st.caption("El círculo se centra en la capital del estado como referencia; "
               "el dataset no incluye la ubicación exacta de los accidentes.")

# TENDENCIA MENSUAL
with col2:
    st.subheader("Tendencia mensual")
    if len(df_filtrado) > 0:
        fig_line = px.line(
            df_filtrado,
            x="mes",
            y=["accidentes", "heridos", "muertos"],
            markers=True,
            labels={"mes": "Mes", "value": "Cantidad", "variable": "Indicador"}
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Selecciona al menos un mes para ver la gráfica.")

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
        size_max=50,
        labels={"heridos": "Heridos",
                "danios_materiales_millones": "Daños materiales (millones)"}
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

# COMPARACIÓN ENTRE ESTADOS (datos reales del mismo archivo)
st.divider()
st.subheader(f"{estado} frente a otros estados")

metrica_nombre = st.selectbox("Comparar por:", list(METRICAS.keys()))
metrica = METRICAS[metrica_nombre]

df_meses = df_all[df_all['mes'].isin(mes_seleccionado)]
if len(df_meses) > 0:
    g = (
        df_meses.groupby('entidad_federativa', observed=True)[['accidentes', 'heridos', 'muertos']]
        .sum()
        .reset_index()
    )
    g['muertos_x100'] = (g['muertos'] / g['accidentes'].where(g['accidentes'] > 0) * 100).fillna(0).round(1)
    g = g.sort_values(metrica, ascending=False).reset_index(drop=True)
    g['lugar'] = g.index + 1

    top = g.head(10)
    if estado not in top['entidad_federativa'].values:
        top = pd.concat([top, g[g['entidad_federativa'] == estado]])

    top = top.copy()
    top['Grupo'] = top['entidad_federativa'].apply(lambda e: estado if e == estado else 'Otros')

    fig_top = px.bar(
        top,
        x=metrica,
        y="entidad_federativa",
        color="Grupo",
        orientation="h",
        color_discrete_map={estado: '#d62728', 'Otros': '#9aa0a6'},
        labels={"entidad_federativa": "Entidad", metrica: metrica_nombre},
        title=f"Top 10 entidades por {metrica_nombre.lower()} (meses seleccionados)"
    )
    fig_top.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_top, use_container_width=True)

    lugar = int(g.loc[g['entidad_federativa'] == estado, 'lugar'].iloc[0])
    st.caption(f"{estado} ocupa el lugar {lugar} de {len(g)} en {metrica_nombre.lower()} "
               "con los meses seleccionados.")
else:
    st.info("Selecciona al menos un mes para ver la comparación.")