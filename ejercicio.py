import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#url = 'https://tp8-59194.streamlit.app/'

st.set_page_config(page_title="parcial", layout="centered", initial_sidebar_state="auto")


st.title("Ingrese un archivo CSV desde la barra lateral")
st.sidebar.title("Archivos de datos")

def mostrar_informacion_alumno():
    with st.container(border=True):
        st.markdown('**Legajo:** 59.194')
        st.markdown('**Nombre:** Medina Maria Josefina')
        st.markdown('**Comisión:** C7')

mostrar_informacion_alumno()

sucursales=["Todas", "Sucursal Norte", "Sucursal Sur", "Sucursal Centro"]
archivo=None
datos=None

archivosCSV = st.sidebar.file_uploader("Sube un archivo csv", type=["csv"])
if archivosCSV:
    archivo = pd.read_csv(archivosCSV)
    #sucursales=["Todas"]+datos["Sucursal"].unique().tolist()
    
seleccionSucursal= st.sidebar.selectbox("Seleccione una sucursal: ", sucursales)
if archivo is not None:
    if seleccionSucursal == "Todas":
        datos=archivo
    else:
        datos =archivo[archivo["Sucursal"] == seleccionSucursal]

    productos= datos["Producto"].unique()

    for producto in productos:
        #with st.container(border=True):
        datosP = datos[datos["Producto"] == producto]
        unidades_vendidas = datosP["Unidades_vendidas"].sum()
        ingreso_total = datosP["Ingreso_total"].sum()
        costo_total = datosP["Costo_total"].sum()
        
        # Calcular precio promedio como en el primer código
        datosP['Precio_promedio'] = datosP['Ingreso_total'] / datosP['Unidades_vendidas']
        precio_promedio = datosP['Precio_promedio'].mean()
        
        margen_promedio = (ingreso_total - costo_total) / ingreso_total
        margenAnual = (datosP.groupby("Año")["Ingreso_total"].sum() - datosP.groupby("Año")["Costo_total"].sum()) / datosP.groupby("Año")["Ingreso_total"].sum()
        
        ventasAnuales = datosP.groupby("Año")["Unidades_vendidas"].sum()
        variacionPorcentual = ventasAnuales.pct_change().iloc[-1] * 100
        
        precioPromedioAnual = datosP.groupby("Año")['Ingreso_total'].sum() / datosP.groupby("Año")['Unidades_vendidas'].sum()
        variacionPrecioPromedio = precioPromedioAnual.pct_change().iloc[-1] * 100
        
        variacionMargenAnual = margenAnual.pct_change().iloc[-1] * 100
            #promedio precio

        with st.container():
                st.markdown("""
                <div style="
                    border: 0.5px solid #ddd;
                    padding: 0.5px;
                    margin-bottom: 10px;
                    border-radius: 4px;
                    background-color: #fafafa;
                    box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);">
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.subheader(producto)
                    st.metric("Precio promedio:", f"${precio_promedio:,.0f}", f"{variacionPrecioPromedio:.2f}%", delta_color="normal")
                    st.metric("Margen promedio:", f"{margen_promedio:.0%}", f"{variacionMargenAnual:.2f}%")
                    st.metric("Unidades Vendidas:", f"{unidades_vendidas:,.0f}", f"{variacionPorcentual:.2f}%")
                
                with col2:
                    ventasMensuales = datosP.groupby(["Año", "Mes"])["Unidades_vendidas"].sum().reset_index()
                    ventasMensuales["Fecha"] = pd.to_datetime(ventasMensuales["Año"].astype(str) + "-" + ventasMensuales["Mes"].astype(str) + "-01")
                    plt.figure(figsize=(10, 7))
                    sns.lineplot(data=ventasMensuales, x="Fecha", y="Unidades_vendidas", label="Ventas Mensuales")
                    z = np.polyfit(range(len(ventasMensuales)), ventasMensuales["Unidades_vendidas"], 1)
                    p = np.poly1d(z)
                    plt.plot(ventasMensuales["Fecha"], p(range(len(ventasMensuales))), label="Tendencia", linestyle="--", color="red")
                    plt.title(f"Evolución de Ventas Mensuales:")
                    plt.xlabel("Año-Mes")
                    plt.ylabel("Unidades Vendidas")
                    plt.legend([f"{producto}", "Tendencia"], loc="upper left")
                    st.pyplot(plt)
        st.markdown("</div>", unsafe_allow_html=True)


            