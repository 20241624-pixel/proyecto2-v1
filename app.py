import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuración inicial de la página
st.set_page_config(
    page_title="CinePulse Ops | Cineplanet",
    page_icon="🍿",
    layout="wide"
)

# Encabezado y rótulo obligatorio de datos simulados
st.title("🍿 CinePulse Ops — Sistema Inteligente de Alerta y Abastecimiento")
st.caption("Plataforma de soporte a la decisión para Administradores de Complejo | Cineplanet (Cineplex S.A.)")

st.warning(
    "⚠️ **AVISO ACADÉMICO (PROTOTIPO FUNCIONAL):** Los datos operativos, tasas de conversión y niveles de inventario mostrados "
    "en esta aplicación son **simulados** con fines demostrativos para el curso de Analítica de Negocios."
)

# --- PANEL LATERAL: ENTRADAS (INPUTS) ---
st.sidebar.header("⚙️ Parámetros del Complejo")

complejo = st.sidebar.selectbox(
    "Complejo Cinematográfico:",
    ["Cineplanet Salaverry", "Cineplanet San Miguel", "Cineplanet Primavera", "Cineplanet Alcázar", "Cineplanet Mall del Sur"]
)

tipo_dia = st.sidebar.selectbox(
    "Escenario de Cartelera:",
    ["Día Regular (Lun-Mie)", "Fin de Semana Regular", "Estreno Blockbuster / Feriado"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🎟️ Datos de Preventa y Piso (Próximas 2 hrs)")

preventa_entradas = st.sidebar.slider(
    "Entradas vendidas / preventa (próximas 2h):",
    min_value=100,
    max_value=1800,
    value=950,
    step=50,
    help="Total de asistentes proyectados en funciones de las próximas 2 horas."
)

stock_canchita = st.sidebar.number_input(
    "Stock actual preparado de Canchita (porciones):",
    min_value=50,
    max_value=1500,
    value=320,
    step=20
)

stock_bebidas = st.sidebar.number_input(
    "Stock disponible de Vasos/Bebidas (unidades):",
    min_value=50,
    max_value=1500,
    value=400,
    step=20
)

cajas_activas = st.sidebar.slider(
    "Cajas de dulcería habilitadas actualmente:",
    min_value=1,
    max_value=10,
    value=4
)

# --- PROCESAMIENTO ANALÍTICO (SIMULACIÓN DE MODELO PREDICTIVO) ---
# Factores según escenario
if tipo_dia == "Día Regular (Lun-Mie)":
    tasa_conversion = 0.34
    ticket_promedio = 26.5
elif tipo_dia == "Fin de Semana Regular":
    tasa_conversion = 0.42
    ticket_promedio = 31.0
else:  # Estreno Blockbuster
    tasa_conversion = 0.48
    ticket_promedio = 34.5

# Ajuste leve por complejo
factor_complejo = {
    "Cineplanet Salaverry": 1.05,
    "Cineplanet San Miguel": 1.03,
    "Cineplanet Primavera": 1.00,
    "Cineplanet Alcázar": 0.96,
    "Cineplanet Mall del Sur": 1.02
}[complejo]

tasa_conversion_ajustada = min(tasa_conversion * factor_complejo, 0.65)

# Cálculos principales
transacciones_estimadas = int(round(preventa_entradas * tasa_conversion_ajustada))
demanda_canchita = int(round(transacciones_estimadas * 1.15))  # Algunos combos llevan 2 porciones
demanda_bebidas = int(round(transacciones_estimadas * 1.35))
ingresos_proyectados = transacciones_estimadas * ticket_promedio

# Capacidad de atención: 1 caja atiende aprox. 40 transacciones por hora (80 en 2 horas)
capacidad_cajas_2h = cajas_activas * 80
cajas_recomendadas = max(1, int(np.ceil(transacciones_estimadas / 80)))

# Brechas de inventario
brecha_canchita = stock_canchita - demanda_canchita
brecha_bebidas = stock_bebidas - demanda_bebidas

# --- SALIDAS: TARJETAS DE KPIs ---
st.subheader(f"📊 Panel Operativo en Tiempo Real — {complejo}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Tasa Conversión Esperada",
        value=f"{tasa_conversion_ajustada*100:.1f}%",
        delta=f"{transacciones_estimadas} transacciones"
    )

with col2:
    st.metric(
        label="Demanda Canchita (2h)",
        value=f"{demanda_canchita} porc.",
        delta=f"{brecha_canchita} vs stock actual",
        delta_color="normal" if brecha_canchita >= 0 else "inverse"
    )

with col3:
    st.metric(
        label="Cajas Recomendadas",
        value=f"{cajas_recomendadas} cajas",
        delta=f"{cajas_recomendadas - cajas_activas:+d} vs activas ({cajas_activas})",
        delta_color="inverse" if cajas_recomendadas > cajas_activas else "normal"
    )

with col4:
    st.metric(
        label="Venta Proyectada Dulcería",
        value=f"S/ {ingresos_proyectados:,.0f}",
        delta=f"Ticket prom: S/ {ticket_promedio:.2f}"
    )

st.markdown("---")

# --- MOTOR DE ALERTAS TEMPRANAS (PRESCRIPTIVO) ---
st.subheader("🚨 Motor de Alertas Tempranas y Acciones Prescriptivas")

alertas_criticas = []
alertas_preventivas = []

if brecha_canchita < 0:
    alertas_criticas.append(
        f"**Quiebre inminente de Canchita:** Faltan **{abs(brecha_canchita)} porciones** para cubrir las próximas 2 horas. "
        f"*Acción:* Activar producción continua en máquinas pop-corn de inmediato."
    )
elif brecha_canchita < 60:
    alertas_preventivas.append(
        f"**Stock ajustado de Canchita:** Margen de seguridad bajo ({brecha_canchita} porciones libres). "
        f"*Acción:* Preparar 1 lote adicional preventivo."
    )

if brecha_bebidas < 0:
    alertas_criticas.append(
        f"**Quiebre inminente de Bebidas/Vasos:** Faltan **{abs(brecha_bebidas)} unidades**. "
        f"*Acción:* Reabastecer dispensadores y vasos desde almacén central."
    )

if cajas_recomendadas > cajas_activas:
    alertas_criticas.append(
        f"**Congestión en Fila Proyectada:** La demanda ({transacciones_estimadas} clientes) supera la capacidad de {cajas_activas} cajas ({capacidad_cajas_2h} clientes). "
        f"*Acción:* Habilitar **{cajas_recomendadas - cajas_activas} caja(s) adicional(es)** o activar fila rápida de combos."
    )

if brecha_canchita > 250 and tipo_dia == "Día Regular (Lun-Mie)":
    alertas_preventivas.append(
        f"**Riesgo de Merma Operativa:** Excedente estimado de **{brecha_canchita} porciones** de canchita respecto a la demanda. "
        f"*Acción:* Pausar producción nueva hasta rotar inventario actual."
    )

if alertas_criticas:
    for alerta in alertas_criticas:
        st.error(f"🔴 **ALERTA CRÍTICA:** {alerta}")
if alertas_preventivas:
    for alerta in alertas_preventivas:
        st.warning(f"🟡 **ALERTA PREVENTIVA:** {alerta}")
if not alertas_criticas and not alertas_preventivas:
    st.success("🟢 **OPERACIÓN ÓPTIMA:** El stock preparado y las cajas habilitadas cubren adecuadamente la demanda proyectada sin riesgo de merma.")

st.markdown("---")

# --- GRÁFICOS INTERACTIVOS POR FRANJA DE 30 MINUTOS ---
st.subheader("📈 Proyección de Demanda vs. Capacidad por Franja Horaria (Bloques de 30 min)")

franjas = ["18:00 - 18:30", "18:30 - 19:00", "19:00 - 19:30", "19:30 - 20:00"]
# Distribución típica del pico antes de funciones estelares
pesos_franja = [0.20, 0.35, 0.30, 0.15]

df_franjas = pd.DataFrame({
    "Franja Horaria": franjas,
    "Asistentes Sala": [int(preventa_entradas * p) for p in pesos_franja],
    "Demanda Canchita (porc.)": [int(demanda_canchita * p) for p in pesos_franja],
    "Clientes Dulcería": [int(transacciones_estimadas * p) for p in pesos_franja],
    "Capacidad Actual Cajas": [int(capacidad_cajas_2h / 4)] * 4
})

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    fig_cajas = go.Figure()
    fig_cajas.add_trace(go.Bar(
        x=df_franjas["Franja Horaria"],
        y=df_franjas["Clientes Dulcería"],
        name="Demanda Esperada (Clientes)",
        marker_color="#E50914"
    ))
    fig_cajas.add_trace(go.Scatter(
        x=df_franjas["Franja Horaria"],
        y=df_franjas["Capacidad Actual Cajas"],
        name="Capacidad Actual Cajas",
        mode="lines+markers",
        line=dict(color="#0033A0", width=3, dash="dash")
    ))
    fig_cajas.update_layout(
        title="Flujo de Clientes vs. Capacidad de Atención en Cajas",
        xaxis_title="Franja Horaria",
        yaxis_title="Clientes",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=380
    )
    st.plotly_chart(fig_cajas, use_container_width=True)

with col_graf2:
    # Stock acumulado restante si no se repone
    stock_restante = []
    acumulado = stock_canchita
    for d in df_franjas["Demanda Canchita (porc.)"]:
        acumulado -= d
        stock_restante.append(acumulado)
    df_franjas["Stock Remanente Canchita"] = stock_restante

    fig_stock = go.Figure()
    fig_stock.add_trace(go.Scatter(
        x=df_franjas["Franja Horaria"],
        y=df_franjas["Stock Remanente Canchita"],
        name="Inventario Remanente (sin reposición)",
        mode="lines+markers+text",
        text=df_franjas["Stock Remanente Canchita"],
        textposition="top center",
        line=dict(color="#FF9900", width=3)
    ))
    fig_stock.add_hline(y=0, line_dash="dot", line_color="red", annotation_text="Nivel de Quiebre (0)")
    fig_stock.update_layout(
        title="Curva de Agotamiento de Canchita (Sin Reposición)",
        xaxis_title="Franja Horaria",
        yaxis_title="Porciones en Stock",
        height=380
    )
    st.plotly_chart(fig_stock, use_container_width=True)

# Tabla de detalle operativo
with st.expander("📋 Ver tabla detallada de proyección por franja horaria"):
    st.dataframe(df_franjas, use_container_width=True, hide_index=True)