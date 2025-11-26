import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

# --- CONFIGURACIÓN DE PÁGINA (Estilo Académico) ---
st.set_page_config(layout="wide", page_title="Fraud Audit Report", page_icon="⚖️")

# --- INYECCIÓN DE CSS (Tu Prompt Maestro) ---
st.markdown("""
<style>
    /* Tipografía Serif Elegante */
    @import url('https://fonts.googleapis.com/css2?family=Georgia:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Georgia', serif;
    }
    
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: bold;
    }
    
    /* Cajas de Texto Personalizadas */
    .report-text {
        text-align: justify;
        font-size: 18px;
        line-height: 1.6;
        color: #333;
        padding: 10px;
    }
    
    .observation-box {
        background-color: #ffffff;
        border-left: 5px solid #2c3e50;
        padding: 15px;
        margin: 20px 0;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    
    .prescription-box {
        background-color: #f0fdf4; /* Verde muy pálido */
        border-left: 5px solid #15803d; /* Verde fuerte */
        padding: 15px;
        margin: 20px 0;
    }
    
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        padding: 20px;
        border-radius: 5px;
        text-align: center;
    }

    /* Matriz Lógica */
    table.logic-matrix {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-family: 'Georgia', serif;
    }
    table.logic-matrix th {
        background-color: #2c3e50;
        color: white;
        padding: 10px;
        text-align: left;
    }
    table.logic-matrix td {
        border-bottom: 1px solid #ddd;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- TÍTULO Y CONTEXTO ---
st.title("🛡️ Sistema de Auditoría de Riesgo Financiero")
st.markdown('<div class="report-text">Este reporte interactivo permite la evaluación probabilística de transacciones bancarias mediante modelos de Machine Learning (XGBoost) entrenados con patrones de comportamiento histórico.</div>', unsafe_allow_html=True)

# --- SIDEBAR: PANEL DE CONTROL ---
st.sidebar.header("🕹️ Simulador de Transacción")
st.sidebar.markdown("---")

# Inputs del usuario (Simulando al cajero o sistema)
amount = st.sidebar.number_input("Monto de la Transacción ($)", min_value=0.0, value=180000.0)
old_bal_org = st.sidebar.number_input("Saldo Inicial (Origen)", min_value=0.0, value=180000.0)
new_bal_org = st.sidebar.number_input("Saldo Final (Origen)", min_value=0.0, value=0.0)
old_bal_dest = st.sidebar.number_input("Saldo Inicial (Destino)", min_value=0.0, value=0.0)
new_bal_dest = st.sidebar.number_input("Saldo Final (Destino)", min_value=0.0, value=0.0)
tx_type = st.sidebar.selectbox("Tipo de Operación", ["TRANSFER", "CASH_OUT", "PAYMENT", "DEBIT"])
hour = st.sidebar.slider("Hora del día (0-23h)", 0, 23, 3)

# Botón de Análisis
analyze_btn = st.sidebar.button("🔍 Ejecutar Auditoría")

# --- LÓGICA DE AUDITORÍA ---
if analyze_btn:
    # 1. Preparar Payload para la API
    payload = {
        "type": tx_type,
        "amount": amount,
        "oldbalanceOrg": old_bal_org,
        "newbalanceOrig": new_bal_org,
        "oldbalanceDest": old_bal_dest,
        "newbalanceDest": new_bal_dest,
        "step": hour
    }
    
    # 2. Llamar a la API
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        result = response.json()
        
        prob = result.get("risk_score", 0)
        is_fraud = result.get("is_fraud", False)
        
        # --- ESTRUCTURA DEL REPORTE CIENTÍFICO ---
        
        # I. DIAGNÓSTICO VISUAL
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Nivel de Riesgo Calculado")
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = prob * 100,
                title = {'text': "Probabilidad de Fraude (%)"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#8B0000" if is_fraud else "#2E8B57"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 100], 'color': "gray"}],
                }
            ))
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("### II. Análisis de Evidencia")
            st.markdown(f"""
            <div class="observation-box">
                <b>Discusión de Resultados:</b><br>
                El modelo ha detectado patrones en la transacción actual con una probabilidad de <b>{prob*100:.2f}%</b>.
                <br><br>
                <b>Factores Críticos Observados:</b>
                <ul>
                    <li>Discrepancia en balance de origen: <b>${(new_bal_org + amount - old_bal_org):.2f}</b></li>
                    <li>Hora de operación: <b>{hour}:00 hrs</b> (Ventana de {hour}h)</li>
                    <li>Tipo de movimiento: <b>{tx_type}</b></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # III. MATRIZ LÓGICA Y ESTRATEGIA (Tu Prompt Maestro)
        st.markdown("### III. Matriz Lógica y Estrategia Prescriptiva")
        
        # Lógica condicional para el texto
        if is_fraud:
            diag = "Patrón anómalo compatible con vaciado de cuenta (Account Takeover)."
            presc = "Bloqueo preventivo inmediato y contacto biométrico con el cliente."
            status_color = "#ffebee" # Rojo suave
        else:
            diag = "Comportamiento transaccional dentro de parámetros normales."
            presc = "Autorizar transacción y registrar en historial positivo."
            status_color = "#e8f5e9" # Verde suave

        st.markdown(f"""
        <table class="logic-matrix">
            <tr>
                <th>Fase Analítica</th>
                <th>Detalle del Hallazgo</th>
            </tr>
            <tr style="background-color: {status_color}">
                <td><b>1. Descriptiva</b> (¿Qué pasó?)</td>
                <td>Transacción de ${amount:,.2f} vía {tx_type}.</td>
            </tr>
            <tr style="background-color: {status_color}">
                <td><b>2. Diagnóstica</b> (¿Por qué?)</td>
                <td>{diag}</td>
            </tr>
            <tr style="background-color: {status_color}">
                <td><b>3. Prescriptiva</b> (¿Qué hacer?)</td>
                <td><b>{presc}</b></td>
            </tr>
        </table>
        
        <div class="prescription-box">
            <b>🏛️ Acción Recomendada:</b><br>
            Basado en la política de riesgo del banco y el umbral de tolerancia (50%), el sistema sugiere:
            <b>{'⛔ DENEGAR' if is_fraud else '✅ APROBAR'}</b> esta operación.
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error de conexión con el motor de IA: {e}")
        st.warning("Asegúrate de que la API (uvicorn) esté corriendo en la terminal.")

else:
    # Estado inicial (Instrucciones)
    st.info("👈 Configure los parámetros de la transacción en el panel lateral y presione 'Ejecutar Auditoría'.")
