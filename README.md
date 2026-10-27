# 🌊 AquaRoute GYE: Smart Flood Early Warning & Dynamic Evacuation System
**IEEE-HKN Hack2Impact 2026 — Nu Zeta Chapter (ESPOL) Challenge**

## 📌 Overview
**AquaRoute GYE** is a hybrid cyber-physical system designed to help Guayaquil anticipate and respond to intense rainfall and urban flooding. It combines macroscopic flood susceptibility analysis (**Google Earth Engine**), resilient community telemetry (**ESP32 + LoRa + Ultrasonic Street Poles & River Buoys**), live meteorological data (**Open-Meteo API**), and automated vehicular/pedestrian rerouting around flooded streets.

## 🛠️ Hardware-in-the-Loop (HIL) Prototype
To validate the end-to-end architecture within the 6-hour hackathon window, we built a scaled physical prototype of an **Intelligent Urban Flood Pole**:
* **Microcontroller:** ESP32 Dev Module (`poste_tina.ino`).
* **Water Level Sensing:** Ultrasonic sensor (HC-SR04) measuring real-time water level rise in a scaled flood basin.
* **Local Traffic Signaling:** Physical LED semaphore (`D22` Green LED = Open Lane / Safe; `D23` Red LED = Flooded Lane / Do Not Enter when water exceeds the 20 cm scaled street threshold).
* **Live Map Integration:** Real-time USB Serial telemetry streaming at 1 Hz into a Python **Streamlit + Folium** geospatial dashboard (`app.py`) that automatically recalculates evacuation routes toward high-ground shelters (Cerro del Carmen) when flooding is detected.

## 🚀 How to Run the Prototype
1. Flash `poste_tina.ino` onto the ESP32 using Arduino IDE.
2. Install Python dependencies:
   ```bash
   pip install streamlit folium streamlit-folium requests pyserial