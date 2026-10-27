// Proyecto: AquaRoute GYE - Poste Inteligente con Semáforo Vial
const int TRIG_PIN = 5;   // Pin D5 para Trigger del HC-SR04
const int ECHO_PIN = 18;  // Pin D18 para Echo del HC-SR04

// Pines para los LEDs en D22 y D23
const int LED_VERDE = 22; // Pin D22: Carril habilitado (Paso libre)
const int LED_ROJO = 23;  // Pin D23: Carril bloqueado por inundación

float alturaTinaVaciaCm = 0.0;
const float ESCALA = 5.0; // 1 cm que sube en tu tina = 5 cm en la calle real

float medirDistancia() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duracion = pulseIn(ECHO_PIN, HIGH, 30000);
  if (duracion == 0) return alturaTinaVaciaCm;
  return (duracion * 0.0343) / 2.0;
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);
  
  delay(1000);
  alturaTinaVaciaCm = medirDistancia();
}

void loop() {
  float distanciaActual = medirDistancia();
  float aguaSubidaCm = alturaTinaVaciaCm - distanciaActual;
  if (aguaSubidaCm < 0.3) aguaSubidaCm = 0.0;

  float nivelCalleCm = aguaSubidaCm * ESCALA;

  // Lógica del semáforo (Umbral de inundación: 20 cm)
  if (nivelCalleCm < 20.0) {
    digitalWrite(LED_VERDE, HIGH);  // Carril seguro -> LED Verde en D22 encendido
    digitalWrite(LED_ROJO, LOW);    // Carril cerrado -> LED Rojo en D23 apagado
  } else {
    digitalWrite(LED_VERDE, LOW);   // Carril seguro -> LED Verde apagado
    digitalWrite(LED_ROJO, HIGH);   // Carril inundado -> LED Rojo en D23 encendido
  }

  Serial.println(nivelCalleCm, 1);
  delay(1000);
}