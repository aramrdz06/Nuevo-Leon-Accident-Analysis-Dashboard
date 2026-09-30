# Dashboard de Accidentes por Estado (enfoque en Nuevo León)

Dashboard interactivo hecho con **Python y Streamlit** para explorar datos de accidentes por entidad federativa y mes, con Nuevo León como estado predeterminado. Proyecto académico de la carrera de Ingeniería en Desarrollo de Software (Tecmilenio).

<!-- Agrega aquí el link de tu app publicada, por ejemplo: **Demo:** https://tu-app.streamlit.app -->
<!-- Agrega aquí una captura de pantalla: sube la imagen al repo y escribe ![Dashboard](captura.png) -->

## Qué permite hacer

- Elegir **cualquiera de los 32 estados** y filtrar por **mes**.
- Ver un resumen con accidentes, heridos, muertos, daños materiales y **muertos por cada 100 accidentes** (indicador calculado a partir de los datos).
- Consultar la **tendencia mensual** de accidentes, heridos y muertos.
- Comparar heridos contra daños materiales en un gráfico de burbujas (el tamaño representa los muertos).
- **Comparar el estado elegido contra el resto del país** en un top 10 por accidentes, heridos, muertos o muertos por cada 100 accidentes, y ver en qué lugar de 32 queda.
- Ver un mapa con el total de accidentes del estado.

## Datos

- **Archivo:** `sct_71_accidentes_mes.csv` (SCT).
- **Contenido:** 384 registros, uno por cada combinación de 32 entidades federativas y 12 meses.
- **Columnas:** `entidad_federativa`, `mes`, `accidentes`, `danios_materiales_millones`, `heridos`, `muertos`.

### Limitaciones

- Los datos vienen **agregados por estado y mes**. No incluyen ubicación exacta, hora ni tipo de accidente, por lo que no se pueden identificar zonas de riesgo dentro de un estado.
- El archivo no trae una columna de año.
- En el mapa, el círculo se coloca en la **capital del estado como referencia**; no representa dónde ocurrieron los accidentes.

## Algunos resultados (Nuevo León, todos los meses del archivo)

| Indicador | Valor | Lugar entre los 32 estados |
|---|---|---|
| Accidentes | 588 | 5° |
| Heridos | 362 | 7° |
| Muertos | 117 | 11° |
| Daños materiales | 69.7 millones | 2° |
| Muertos por cada 100 accidentes | 19.9 | 24° (promedio nacional: 24.6) |

- El mes con más accidentes fue **junio** (60) y el de menos, **septiembre** (32).
- El mes con más muertos fue **enero** (20).

## Tecnologías

Python · Streamlit · Pandas · Plotly · Folium (streamlit-folium)

## Cómo ejecutarlo en tu computadora

```bash
git clone https://github.com/aramrdz06/Nuevo-Leon-Accident-Analysis-Dashboard
cd Nuevo-Leon-Accident-Analysis-Dashboard
pip install -r requirements.txt
streamlit run app.py
```

## Estructura del proyecto

```
├── app.py                      # Aplicación de Streamlit
├── sct_71_accidentes_mes.csv   # Datos
├── requirements.txt            # Dependencias
└── README.md
```

## Autor

Francisco Aram Rodríguez García · [GitHub](https://github.com/aramrdz06)