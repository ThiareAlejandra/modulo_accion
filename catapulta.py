#include <Servo.h>

Servo servoDesbloqueo;  // Servomotor para desbloquear la catapulta (pin 9)
Servo servoLanzamiento; // Servomotor para el lanzamiento (pin 10)

const int anguloDesbloqueo = 90;   // Ángulo para desbloquear la catapulta
const int anguloLanzamiento = 80; // Ángulo para lanzar
const int anguloReposo = 0;        // Ángulo de reposo para ambos servos

const int botonPin = 2; // Pin al que está conectado el botón

unsigned long tiempoUltimoLanzamiento = 0;
const unsigned long intervaloEntreLanzamientos = 1000; // 1 segundo

void setup() {
  servoDesbloqueo.attach(9); // Servomotor de desbloqueo en el pin 9
  servoLanzamiento.attach(10); // Servomotor de lanzamiento en el pin 10

  pinMode(botonPin, INPUT_PULLUP); // Configura el pin del botón como entrada con resistencia pull-up interna
  
  // Inicializa los servos en posición de reposo
  servoDesbloqueo.write(anguloReposo);
  servoLanzamiento.write(anguloReposo);
  
  delay(1000); // Espera 2 segundos antes de iniciar
}

void loop() {
  unsigned long tiempoActual = millis();
  
  if (digitalRead(botonPin) == LOW && (tiempoActual - tiempoUltimoLanzamiento) >= intervaloEntreLanzamientos) {
    lanzarProyectil();
    tiempoUltimoLanzamiento = tiempoActual;
  }
}

void lanzarProyectil() {
  // Mueve el servomotor de lanzamiento
  servoLanzamiento.write(anguloLanzamiento);
  delay(250); // Mantiene el lanzamiento por 0.25 segundos

  // Espera 1 segundo antes de activar el desbloqueo
  delay(1000);
  servoDesbloqueo.write(anguloDesbloqueo); // Mueve el servo de desbloqueo
  
  // Espera 2 segundos antes de mover el servo de lanzamiento a la posición de reposo
  delay(2000);
  
  // Regresa el servomotor de lanzamiento a la posición de reposo
  moverServo(servoLanzamiento, anguloLanzamiento, anguloReposo);
  
  // Regresa el servomotor de desbloqueo a la posición de reposo
  moverServo(servoDesbloqueo, anguloDesbloqueo, anguloReposo);
}

void moverServo(Servo& servo, int anguloInicio, int anguloFin) {
  int delayTime = 10;
  if (anguloInicio > anguloFin) {
    for (int pos = anguloInicio; pos >= anguloFin; pos--) {
      servo.write(pos);
      delay(delayTime); // Ajusta el retraso para cambiar la velocidad del movimiento
    }
  } else {
    for (int pos = anguloInicio; pos <= anguloFin; pos++) {
      servo.write(pos);
      delay(delayTime); // Ajusta el retraso para cambiar la velocidad del movimiento
    }
  }
}
