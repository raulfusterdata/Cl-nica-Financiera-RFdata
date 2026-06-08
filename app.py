import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# ⚙️ CONFIGURACIÓN DE CORREO ELECTRÓNICO
# ==========================================
# IMPORTANTE: No uses tu contraseña normal de Gmail. Debes usar una "Contraseña de Aplicación" (Instrucciones abajo)
EMAIL_REMITENTE = "raulfusterdata@gmail.com"  # Pon aquí tu Gmail
PASSWORD_APP = "vulr bwou farc oryf" # Pon aquí la contraseña generada por Google
EMAIL_DESTINO = "raulfusterdata@gmail.com"    # Dónde quieres recibir los leads (puede ser el mismo)

# ==========================================
# ⚙️ CONFIGURACIÓN Y ESTILOS UX EXTREMA
# ==========================================
st.set_page_config(page_title="RFData - Clínica Financiera", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 12px; height: 4em; font-weight: bold; background-color: #0ea5e9; color: white; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #0284c7; transform: scale(1.02); }
    .card-resumen { background-color: white; border: 1px solid #e2e8f0; padding: 25px; border-radius: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .section-header { color: #0f172a; border-bottom: 2px solid #0ea5e9; padding-bottom: 5px; margin-top: 25px; margin-bottom: 15px; font-weight: bold; font-size: 20px; }
    .metric-box { text-align: center; padding: 15px; background: #f0f9ff; border-radius: 10px; border: 1px solid #bae6fd; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 MOTOR DE ESTADO (PERSISTENCIA TOTAL)
# ==========================================
def inicializar_estado(clave, valor_inicial):
    if clave not in st.session_state:
        st.session_state[clave] = valor_inicial

# Variables maestras del sistema
variables_maestras = {
    'cliente_nombre': "", 'cliente_edad': 24, 'cliente_localidad': "",
    'cliente_dependientes': "Ninguno", 'cliente_experiencia': "Ninguna",
    'cliente_riesgo': "Esperar (Tranquilidad)", 'cliente_motivo': "", 'cliente_expectativas': "",
    'm1_ingresos': 0, 'm1_fijos': 0, 'm1_ocio': 0, 'm1_deuda': 0, 
    'm1_meses_colchon': 6,
    'm2_cap': 0, 'm2_inf': 3.0, 'm2_anios': 10, 'm3_anios': 20,
    'ahorro_real_detectado': 0, 'voluntad_inversion': 0, 'exceso_liquidez': 0, 
    'enviado': False
}
for k, v in variables_maestras.items():
    inicializar_estado(k, v)

# ==========================================
# 🚀 FUNCIÓN DE ENVÍO DE EMAIL
# ==========================================
def enviar_email_lead(datos):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMITENTE
    msg['To'] = EMAIL_DESTINO
    msg['Subject'] = f"🚀 NUEVO LEAD RFData: {datos.get('Nombre', 'Cliente')}"

    # Crear una tabla HTML bonita para que lo leas perfecto en el móvil
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #0ea5e9;">Nueva Auditoría Financiera Recibida</h2>
        <p>Se acaba de registrar un nuevo cliente en la plataforma DIY.</p>
        <table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; max-width: 600px;">
    """
    for clave, valor in datos.items():
        html_body += f"<tr><td style='background-color: #f8fafc; font-weight: bold; width: 40%;'>{clave}</td><td>{valor}</td></tr>"
    
    html_body += """
        </table>
        <p style="color: #64748b; font-size: 12px; margin-top: 20px;">Generado automáticamente por RFData System.</p>
      </body>
    </html>
    """
    
    msg.attach(MIMEText(html_body, 'html'))

    # Conexión al servidor de Google y envío
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_REMITENTE, PASSWORD_APP)
        server.send_message(msg)

# ==========================================
# 🗺️ NAVEGACIÓN DIY
# ==========================================
with st.sidebar:
    st.title("📊 RFData DIY")
    st.caption("Planificación Patrimonial v4.0")
    st.markdown("---")
    menu = st.radio("Ruta de Consultoría:", [
        "📍 Ficha de Inicio", 
        "🩺 Step 1: Tus Flujos de Caja", 
        "🗺️ Step 2: Tu Coste de Inacción", 
        "📈 Step 3: Tu Simulación de Futuro", 
        "🧠 Step 4: Tu Plan Operativo", 
        "📋 Step 5: Resumen y Enviar"
    ])
    st.markdown("---")
    st.info("Completa los pasos en orden. Tus datos se consolidarán en la pestaña final.")

# ==========================================
# 📍 PESTAÑA: FICHA DE INICIO
# ==========================================
if menu == "📍 Ficha de Inicio":
    st.title("📍 Situación Inicial")
    st.info("👋 Bienvenido a tu clínica financiera. Empecemos por conocer tu perfil y contexto personal.")
    
    colA, colB = st.columns(2)
    with colA:
        st.session_state.cliente_nombre = st.text_input("¿Cómo te llamas?", value=st.session_state.cliente_nombre)
        st.session_state.cliente_edad = st.number_input("¿Qué edad tienes?", 18, 100, st.session_state.cliente_edad)
        st.session_state.cliente_localidad = st.text_input("Localidad de residencia", value=st.session_state.cliente_localidad)

    with colB:
        st.session_state.cliente_dependientes = st.selectbox("Personas a tu cargo", ["Ninguno", "1 persona", "2 o más", "Familiares mayores"])
        st.session_state.cliente_experiencia = st.selectbox("Experiencia invirtiendo", ["Ninguna", "Básica (Depósitos)", "Intermedia (Fondos)", "Avanzada"])
        st.session_state.cliente_riesgo = st.selectbox("Perfil ante caídas de bolsa", ["Vender todo (Pánico)", "Esperar (Tranquilidad)", "Comprar más (Oportunidad)"])

    st.session_state.cliente_motivo = st.text_area("¿Qué te preocupa hoy de tu dinero?", value=st.session_state.cliente_motivo)
    st.session_state.cliente_expectativas = st.text_area("¿Cuál es tu gran objetivo o meta vital?", value=st.session_state.cliente_expectativas)

# ==========================================
# 🩺 PESTAÑA: STEP 1 (FLUJOS Y SEGURIDAD RECOMENDADA)
# ==========================================
elif menu == "🩺 Step 1: Tus Flujos de Caja":
    st.title("🩺 Auditoría de Flujos y Seguridad")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.session_state.m1_ingresos = st.number_input("Ingresos Mensuales Netos (€)", value=st.session_state.m1_ingresos, step=100)
        st.session_state.m1_fijos = st.number_input("Costes de Supervivencia (€)", value=st.session_state.m1_fijos, step=50)
        st.session_state.m1_ocio = st.number_input("Calidad de Vida / Ocio (€)", value=st.session_state.m1_ocio, step=50)
        st.session_state.m1_deuda = st.number_input("Cuotas de Deuda activa (€)", value=st.session_state.m1_deuda, step=50)
        st.session_state.m2_cap = st.number_input("Liquidez total en el banco (€)", value=st.session_state.m2_cap, step=1000)
        
        st.markdown("---")
        st.session_state.m1_meses_colchon = st.radio("¿Qué nivel de Fondo de Emergencia prefieres?", [3, 6], index=1 if st.session_state.m1_meses_colchon == 6 else 0)

    gastos_obligatorios = st.session_state.m1_fijos + st.session_state.m1_deuda
    st.session_state.ahorro_real_detectado = st.session_state.m1_ingresos - (st.session_state.m1_fijos + st.session_state.m1_ocio + st.session_state.m1_deuda)
    f_3m = gastos_obligatorios * 3
    f_6m = gastos_obligatorios * 6
    colchon_elegido = gastos_obligatorios * st.session_state.m1_meses_colchon
    st.session_state.colchon_objetivo = colchon_elegido
    st.session_state.exceso_liquidez = max(0, st.session_state.m2_cap - colchon_elegido)

    with col2:
        st.markdown(f"""
        <div class='metric-container'>
            <p style='margin:0; color:#64748b; font-weight:bold;'>Rango de Seguridad Profesional Sugerido:</p>
            <h3 style='margin:0; color:#0ea5e9; font-size:1.85rem;'>{f_3m:,.0f}€ - {f_6m:,.0f}€</h3>
        </div><br>
        """, unsafe_allow_html=True)
        st.metric("Capacidad de Ahorro Mensual Máxima", f"{st.session_state.ahorro_real_detectado:,.0f} €")

        if st.session_state.m2_cap >= colchon_elegido:
            st.success(f"✅ Fondo cubierto. Tienes **{st.session_state.exceso_liquidez:,.0f}€** listos para ser invertidos.")
        else:
            st.warning(f"🚨 Te faltan **{colchon_elegido - st.session_state.m2_cap:,.0f}€** para consolidar tu objetivo de seguridad.")

# ==========================================
# 🗺️ PESTAÑA: STEP 2 - COSTE DE INACCIÓN
# ==========================================
elif menu == "🗺️ Step 2: Tu Coste de Inacción":
    st.title("🗺️ El Mapa de la Inflación")
    col1, col2 = st.columns([1, 2])
    with col1:
        cap = st.session_state.m2_cap
        inf_pct = st.slider("Tasa de Inflación Anual Estimada (%)", 1.0, 10.0, 3.0, step=0.1)
        st.session_state.m2_inf = inf_pct
        anios = st.slider("Horizonte de Análisis (Años)", 1, 30, st.session_state.m2_anios)
        st.session_state.m2_anios = anios
    
    with col2:
        t = np.arange(0, anios + 1)
        val_real = cap / ((1 + inf_pct/100)**t)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t, y=val_real, mode='lines', name='Poder de Compra Real', line=dict(color="#ef4444", width=4)))
        fig.update_layout(title="Evolución del Poder de Compra Neto", template="simple_white", height=400)
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 📈 PESTAÑA: STEP 3 - PRUDENCIA FINANCIERA
# ==========================================
elif menu == "📈 Step 3: Tu Simulación de Futuro":
    st.title("📈 Coeficiente de Prudencia Financiera")
    st.markdown("<div class='card-pro'><b>💡 Recomendación:</b> No inviertas el 100% de tu ahorro. Deja un margen de caja libre cada mes.</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Ahorro Máximo Disponible", f"{st.session_state.ahorro_real_detectado:,.0f} €/mes")
    with col2:
        st.session_state.voluntad_inversion = st.number_input(
            "¿Qué cantidad mensual decides activar para tu plan patrimonial? (€)", 
            min_value=0, max_value=max(0, int(st.session_state.ahorro_real_detectado)),
            value=int(st.session_state.ahorro_real_detectado * 0.7)
        )
    st.session_state.m3_anios = st.slider("Años dedicados a la capitalización", 5, 40, st.session_state.m3_anios)

# ==========================================
# 🧠 PESTAÑA: STEP 4 - HOJA DE RUTA TÉCNICA
# ==========================================
elif menu == "🧠 Step 4: Tu Plan Operativo":
    st.title("🧠 Hoja de Ruta de Ejecución")
    st.markdown(f"""
    <div class='card-resumen'>
    <h3>Plan Inmediato:</h3>
    <ol>
        <li><b>Activación del Excedente:</b> Despliegue del capital estancado de (**{st.session_state.exceso_liquidez:,.0f}€**).</li>
        <li><b>Estrategia DCA:</b> Automatización de **{st.session_state.voluntad_inversion:,.0f}€** los días 1 de cada mes.</li>
        <li><b>Seguridad:</b> Aislamiento absoluto del colchón fijado de **{st.session_state.colchon_objetivo:,.0f}€**.</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 📋 PESTAÑA: STEP 5 - RESUMEN Y ENVÍO POR EMAIL
# ==========================================
elif menu == "📋 Step 5: Resumen y Enviar":
    st.title("📋 Consolidación de Datos de Auditoría")
    
    if not st.session_state.enviado:
        st.markdown("Verifica minuciosamente la integridad de los datos antes de proceder al envío a tu consultor.")
        
        # CATEGORÍA 1: CUALITATIVO
        st.markdown("<div class='section-header'>1. CONTEXTO CUALITATIVO Y PERFIL DE CLIENTE</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.write(f"**Nombre:** {st.session_state.cliente_nombre}")
        c2.write(f"**Edad:** {st.session_state.cliente_edad} años")
        c3.write(f"**Localidad:** {st.session_state.cliente_localidad}")
        st.write(f"**Preocupación:** {st.session_state.cliente_motivo}")
        st.write(f"**Meta:** {st.session_state.cliente_expectativas}")

        # CATEGORÍA 2: RADIOGRAFÍA DE FLUJOS
        st.markdown("<div class='section-header'>2. INDICADORES CUANTITATIVOS MENSUALES</div>", unsafe_allow_html=True)
        f1, f2, f3, f4 = st.columns(4)
        f1.write(f"**Ingresos Netos:** {st.session_state.m1_ingresos:,.0f} €")
        f2.write(f"**Costes Fijos:** {st.session_state.m1_fijos:,.0f} €")
        f3.write(f"**Consumo Ocio:** {st.session_state.m1_ocio:,.0f} €")
        f4.write(f"**Deudas:** {st.session_state.m1_deuda:,.0f} €")

        # CATEGORÍA 3: SEGURIDAD
        st.markdown("<div class='section-header'>3. MÉTRICAS DE SEGURIDAD Y ASIGNACIÓN</div>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown(f"<div class='metric-box'><b>Ahorro Máximo</b><br>{st.session_state.ahorro_real_detectado:,.0f} €/mes</div>", unsafe_allow_html=True)
        with s2:
            st.markdown(f"<div class='metric-box'><b>Fondo Elegido</b><br>{st.session_state.m1_meses_colchon} meses ({st.session_state.colchon_objetivo:,.0f} €)</div>", unsafe_allow_html=True)
        with s3:
            st.markdown(f"<div class='metric-box'><b>Exceso a invertir</b><br>{st.session_state.exceso_liquidez:,.0f} €</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # BOTÓN DE ENVÍO AUTOMÁTICO POR EMAIL
        if st.button("🚀 ENVIAR AUDITORÍA A MI CONSULTOR"):
            with st.spinner("Conectando con el servidor seguro y enviando datos..."):
                try:
                    # RECOPILACIÓN DE DATOS
                    registro_completo = {
                        "Fecha_Hora": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Nombre": st.session_state.cliente_nombre,
                        "Edad": f"{st.session_state.cliente_edad} años",
                        "Localidad": st.session_state.cliente_localidad,
                        "Personas_Cargo": st.session_state.cliente_dependientes,
                        "Experiencia_Inversion": st.session_state.cliente_experiencia,
                        "Perfil_Riesgo": st.session_state.cliente_riesgo,
                        "Motivo_Consulta": st.session_state.cliente_motivo,
                        "Meta_Financiera": st.session_state.cliente_expectativas,
                        "Ingresos_Mensuales": f"{st.session_state.m1_ingresos} €",
                        "Gastos_Fijos": f"{st.session_state.m1_fijos} €",
                        "Gastos_Ocio": f"{st.session_state.m1_ocio} €",
                        "Gastos_Deuda": f"{st.session_state.m1_deuda} €",
                        "Ahorro_Max_Detectado": f"{st.session_state.ahorro_real_detectado} €",
                        "Meses_Fondo_Elegido": f"{st.session_state.m1_meses_colchon} meses",
                        "Objetivo_Fondo_Seguridad": f"{st.session_state.colchon_objetivo} €",
                        "Liquidez_Actual_Banco": f"{st.session_state.m2_cap} €",
                        "Exceso_Capital_Estancado": f"{st.session_state.exceso_liquidez} €",
                        "Voluntad_Inversion_Mensual": f"{st.session_state.voluntad_inversion} €",
                        "Margen_Caja_Libre_Mensual": f"{(st.session_state.ahorro_real_detectado - st.session_state.voluntad_inversion)} €",
                        "Horizonte_Inversion_Anios": f"{st.session_state.m3_anios} años"
                    }
                    
                    # Llamada a la función de email
                    enviar_email_lead(registro_completo)
                    
                    time.sleep(1)
                    st.session_state.enviado = True
                    st.rerun()
                    
                except smtplib.SMTPAuthenticationError:
                    st.error("❌ **Error de Autenticación de Correo:** La contraseña de Gmail o el correo configurados en el código son incorrectos. Recuerda usar una Contraseña de Aplicación de 16 caracteres.")
                except Exception as e:
                    st.error(f"Fallo crítico al enviar el email: {e}")

    else:
        # INTERFAZ FINAL DE CONFIRMACIÓN
        st.balloons()
        st.markdown(f"""
            <div style='text-align: center; padding: 50px; background-color: white; border-radius: 15px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);'>
                <h1 style='color: #22c55e; font-size: 2.5rem; margin-bottom: 20px;'>¡Auditoría Patrimonial Recibida!</h1>
                <p style='font-size: 1.25em; color: #334155; margin-bottom: 10px;'>Hola <b>{st.session_state.cliente_nombre}</b>, tus datos clínicos han sido enviados a tu consultor asignado.</p>
                <p style='color: #64748b; font-size: 1.05em; max-width: 700px; margin: 0 auto 30px auto;'>Nuestros especialistas analizarán tu estructura financiera para confeccionar tu <b>Informe de Planificación Patrimonial a medida</b>. Recibirás tu documento estratégico directamente en tu email.</p>
                <hr style='border: 0; border-top: 1px solid #e2e8f0; margin-bottom: 30px;'>
                <p style='color: #94a3b8; font-size: 0.9rem;'><i>Ya puedes cerrar esta pestaña de forma segura. Gracias por tu confianza.</i></p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅️ Volver a verificar mis respuestas"):
            st.session_state.enviado = False
            st.rerun()