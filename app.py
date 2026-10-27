import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import serial

st.set_page_config(page_title="Guayaquil Flood Evacuation Prototype", layout="wide")

# 1. API de Clima Real para Guayaquil (Open-Meteo)
def obtener_clima_guayaquil():
    url = "https://api.open-meteo.com/v1/forecast?latitude=-2.1894&longitude=-79.8891&current=precipitation,temperature_2m&timezone=America%2FGuayaquil"
    try:
        r = requests.get(url, timeout=4).json()
        return r["current"]["precipitation"], r["current"]["temperature_2m"]
    except Exception:
        return 35.0, 24.0

st.sidebar.header("🔌 Urban Pole Prototype (Tub Test)")
modo_usb = st.sidebar.toggle("Connect Live HC-SR04 Sensor (USB)", value=False)
puerto_usb = st.sidebar.text_input("USB Port (e.g. COM3)", value="COM3")

if "nivel_agua" not in st.session_state:
    st.session_state.nivel_agua = 0.0

# 2. BLOQUE PRINCIPAL ENTIEMPO REAL (Se actualiza todo solo cada 1 segundo)
@st.fragment(run_every=1)
def dashboard_en_tiempo_real():
    # Leer el sensor por USB de forma automática
    if modo_usb:
        try:
            with serial.Serial(puerto_usb, 115200, timeout=1) as ser:
                ser.reset_input_buffer()
                linea = ser.readline().decode("utf-8", errors="ignore").strip()
                if linea:
                    st.session_state.nivel_agua = float(linea)
        except Exception:
            pass # Ignora micro-cortes para no congelar la pantalla

    # Selector manual o lectura en vivo
    if not modo_usb:
        nivel_calle = st.sidebar.slider("Test Water Level in Street [cm] (Manual)", 0.0, 60.0, 5.0, key="slider_manual")
    else:
        nivel_calle = st.session_state.nivel_agua
        st.sidebar.metric("Live Tub Sensor Reading", f"{nivel_calle:.1f} cm")

    # TÍTULO Y MÉTRICAS PRINCIPALES
    st.title("🌊 Smart Flood Detection & Evacuation Route Prototype - Guayaquil")
    lluvia_mm, temp_c = obtener_clima_guayaquil()
    inundado = nivel_calle >= 20.0  # Si sube de 20 cm, activa alerta roja y desvío

    c1, c2, c3 = st.columns(3)
    c1.metric("📏 Street Pole Water Level", f"{nivel_calle:.1f} cm", "FLOOD ALERT!" if inundado else "SAFE LEVEL")
    c2.metric("🌧️ Live Guayaquil Rain (Open-Meteo)", f"{lluvia_mm} mm", f"{temp_c} °C")
    c3.metric("🚗 Traffic & Evacuation Action", "REROUTE ACTIVE" if inundado else "NORMAL ROUTE", "Avoid Downtown" if inundado else "Clear")

    # MAPA DINÁMICO DE GUAYAQUIL (Se redibuja solo con el nuevo nivel)
    pos_poste = [-2.1905, -79.8865]      # Centro (Av. 9 de Octubre)
    origen_carro = [-2.2010, -79.8880]   # Zona comercial baja
    refugio_seguro = [-2.1790, -79.8805] # Zona alta (Cerro del Carmen)

    if inundado:
        # Ruta alternativa rodeando la zona inundada
        ruta = [origen_carro, [-2.1985, -79.8950], [-2.1890, -79.9015], [-2.1810, -79.8920], refugio_seguro]
        color_ruta = "orange"
    else:
        # Ruta directa normal
        ruta = [origen_carro, pos_poste, [-2.1850, -79.8830], refugio_seguro]
        color_ruta = "blue"

    m = folium.Map(location=[-2.1895, -79.8890], zoom_start=14)

    folium.Marker(
        pos_poste,
        tooltip=f"Urban Pole Sensor: {nivel_calle:.1f} cm",
        icon=folium.Icon(color="red" if inundado else "green", icon="warning-sign" if inundado else "info-sign")
    ).add_to(m)

    if inundado:
        folium.Circle(pos_poste, radius=450, color="red", fill=True, fill_opacity=0.4, popup="FLOODED STREET - DO NOT ENTER").add_to(m)

    folium.Marker(origen_carro, tooltip="Vehicle Origin", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker(refugio_seguro, tooltip="Safe High Ground (Cerro del Carmen)", icon=folium.Icon(color="darkgreen")).add_to(m)
    folium.PolyLine(ruta, color=color_ruta, weight=6, tooltip="Evacuation Route").add_to(m)

    # Se agrega una clave dinámica basada en el nivel para forzar la actualización visual del mapa
    st_folium(m, width=900, height=480, key=f"map_dynamic_{nivel_calle}")

# Ejecutar el tablero interactivo automático
dashboard_en_tiempo_real()