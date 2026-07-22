import streamlit as st
import requests

# Configuración de la interfaz web
st.set_page_config(
    page_title="Orquestador ML - Diagnóstico Médico",
    page_icon="⚕️",
    layout="wide"
)

# URL del Orquestador FastAPI (Ajusta el puerto si tu backend usa otro)
FASTAPI_URL = "http://localhost:8000"

st.title("⚕️ Sistema Multiparadigma de Diagnóstico Clínico")
st.markdown("""
Esta interfaz se conecta al **Orquestador FastAPI**, el cual delega las predicciones 
a módulos independientes ejecutados en distintos paradigmas de programación mediante **gRPC**.
""")

# --- PESTAÑAS POR DIAGNÓSTICO ---
tab1, tab2, tab3 = st.tabs([
    "❤️ Riesgo Cardíaco (Imperativo - C++)", 
    "🩸 Diabetes (Estructurado - C)", 
    "🎗️ Cáncer de Mama (POO - TS)"
])

# ==========================================
# 1. PESTAÑA: RIESGO CARDÍACO (C++ - Regresión Logística)
# ==========================================
# ==========================================
# 1. PESTAÑA: RIESGO CARDÍACO (C++ - Regresión Logística)
# ==========================================
with tab1:
    st.header("Análisis de Probabilidad de Ataque Cardíaco")
    st.info("Procesado por el módulo **Imperativo (C++)** usando Regresión Logística sobre heart_disease.csv. Precisión: ~70%")
    
    with st.form("form_heart"):
        col1, col2, col3 = st.columns(3)
        with col1:
            edad = st.number_input("Edad", min_value=1, max_value=120, value=45, key="h_age")
            colesterol = st.number_input("Colesterol (mg/dl)", min_value=100, max_value=500, value=200)
        with col2:
            presion = st.number_input("Presión Arterial en Reposo", min_value=80, max_value=200, value=120)
            azucar_ayunas = st.selectbox("¿Azúcar en ayunas > 120 mg/dl?", ["No", "Sí"])
        with col3:
            frecuencia_max = st.number_input("Frecuencia Cardíaca Máxima", min_value=60, max_value=220, value=150)
            angina = st.selectbox("¿Angina inducida por ejercicio?", ["No", "Sí"])
            
        btn_heart = st.form_submit_button("Evaluar Riesgo Cardíaco")
        
        if btn_heart:
            # Mapeo exacto de las 11 columnas segun heart_disease.csv:
            # 1. age, 2. sex, 3. chest_pain_type, 4. resting_bp_s, 5. cholesterol, 
            # 6. fasting_blood_sugar, 7. resting_ecg, 8. max_heart_rate, 
            # 9. exercise_angina, 10. oldpeak, 11. ST_slope
            features_11 = [
                float(edad),                                   # 1. age
                1.0,                                           # 2. sex (1 = Hombre / Neutro)
                2.0,                                           # 3. chest pain type (2 = Neutro)
                float(presion),                                # 4. resting bp s
                float(colesterol),                             # 5. cholesterol
                1.0 if azucar_ayunas == "Sí" else 0.0,         # 6. fasting blood sugar
                0.0,                                           # 7. resting ecg (0 = Normal)
                float(frecuencia_max),                         # 8. max heart rate
                1.0 if angina == "Sí" else 0.0,                # 9. exercise angina
                0.0,                                           # 10. oldpeak (0.0 = Normal)
                1.0                                            # 11. ST slope (1 = Normal)
            ]

            payload = {
                "algorithm": "imperative",
                "features": features_11
            }
            
            with st.spinner("Enviando parámetros al Orquestador FastAPI..."):
                try:
                    response = requests.post(f"{FASTAPI_URL}/predict", json=payload)
                    if response.status_code == 200:
                        resultado = response.json()
                        probabilidad = resultado.get("prediction", 0.0) * 100
                        
                        if probabilidad > 50:
                            st.error(f"⚠️ Alto Riesgo Detectado. Probabilidad de afección cardíaca: {probabilidad:.2f}%")
                        else:
                            st.success(f"✅ Bajo Riesgo Detectado. Probabilidad de afección cardíaca: {probabilidad:.2f}%")
                    else:
                        st.error(f"Error en el orquestador central: Código {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Error de conexión: Asegúrate de que el Orquestador FastAPI esté corriendo.")

# ==========================================
# 2. PESTAÑA: DIABETES (C - KNN)
# ==========================================
with tab2:
    st.header("Clasificación de Pacientes Diabéticos")
    st.info("Procesado por el módulo **Estructurado (C)** usando K-Vecinos Más Cercanos (KNN) sobre diabetes.csv.")
    
    with st.form("form_diabetes"):
        col1, col2 = st.columns(2)
        with col1:
            embarazos = st.number_input("Número de Embarazos", min_value=0, max_value=20, value=0)
            glucosa = st.number_input("Concentración de Glucosa (2h)", min_value=0, max_value=300, value=120)
            presion_diab = st.number_input("Presión Arterial Diastólica (mm Hg)", min_value=0, max_value=150, value=70)
            insulina = st.number_input("Insulina sérica (mu U/ml)", min_value=0, max_value=900, value=80)
        with col2:
            espesor_piel = st.number_input("Espesor del pliegue cutáneo (mm)", min_value=0, max_value=100, value=20)
            bmi = st.number_input("Índice de Masa Corporal (BMI)", min_value=0.0, max_value=70.0, value=25.0)
            pedigree = st.number_input("Función de Pedigrí de Diabetes", min_value=0.0, max_value=3.0, value=0.5)
            edad_diab = st.number_input("Edad (Años)", min_value=1, max_value=120, value=30)
            
        btn_diabetes = st.form_submit_button("Clasificar Paciente")
        
        if btn_diabetes:
            payload = {
                "algorithm": "knn",
                "features": [
                    float(embarazos), float(glucosa), float(presion_diab), float(espesor_piel), 
                    float(insulina), float(bmi), float(pedigree), float(edad_diab)
                ]
            }
            
            with st.spinner("Consultando módulo estructurado en C..."):
                try:
                    response = requests.post(f"{FASTAPI_URL}/predict", json=payload)
                    if response.status_code == 200:
                        resultado = response.json()
                        clase = resultado.get("class")
                        
                        if clase == 1:
                            st.error("🚨 Resultado KNN: El modelo clasifica al paciente como DIABÉTICO.")
                        else:
                            st.success("🟢 Resultado KNN: El modelo clasifica al paciente como NO DIABÉTICO.")
                    else:
                        st.error(f"Error en el servidor central: Código {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Error: El Orquestador FastAPI no responde.")

# ==========================================
# 3. PESTAÑA: CÁNCER DE MAMA (TypeScript - MLP)
# ==========================================
with tab3:
    st.header("Diagnóstico de Cáncer de Mama (Red Neuronal)")
    st.info("Procesado por el módulo **Orientado a Objetos (TypeScript)** mediante un Perceptrón Multicapa (MLP). Precisión: 98.84%")
    
    with st.form("form_mlp"):
        st.write("Ingrese las características geométricas extraídas del núcleo celular:")
        col1, col2, col3 = st.columns(3)
        with col1:
            radio = st.number_input("Radio Medio", value=14.11)
            textura = st.number_input("Textura Media", value=19.22)
        with col2:
            perimetro = st.number_input("Perímetro Medio", value=91.80)
            area = st.number_input("Área Media", value=649.30)
        with col3:
            suavidad = st.number_input("Suavidad Media", value=0.10)
            concavidad = st.number_input("Concavidad Media", value=0.08)
            
        btn_mlp = st.form_submit_button("Ejecutar Predicción de Red Neuronal")
        
        if btn_mlp:
            payload = {
                "algorithm": "mlp",
                "features": [float(radio), float(textura), float(perimetro), float(area), float(suavidad), float(concavidad)]
            }
            
            with st.spinner("Procesando en la Red Neuronal (Módulo POO)..."):
                try:
                    response = requests.post(f"{FASTAPI_URL}/predict", json=payload)
                    if response.status_code == 200:
                        resultado = response.json()
                        diagnostico = resultado.get("prediction")
                        
                        if str(diagnostico).lower() in ["maligno", "1", "positive"]:
                            st.error("⚠️ Alerta MLP: Diagnóstico compatible con Tumor Maligno.")
                        else:
                            st.success("🍏 Diagnóstico MLP: Estructura celular compatible con Tumor Benigno.")
                    else:
                        st.error(f"Error en el orquestador: Código {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Error: Conexión rechazada con el endpoint de FastAPI.")