#include <Servo.h>

// Crear objetos Servo
Servo servoPan;
Servo servoTilt;

// Variables para los ángulos de los servos
int panAngle = 90;  // Posición inicial
int tiltAngle = 90;  // Posición inicial

// Definir los pines de los servos
const int panPin = 3;
const int tiltPin = 5;
//const int ledManualPin = 7;
//const int ledAutoPin = 9;

void setup() {
  // Iniciar comunicación serial
  Serial.begin(9600);
  Serial.setTimeout(10);

  // Adjuntar los servos a los pines
  servoPan.attach(panPin);
  servoTilt.attach(tiltPin);

  // Configurar los pines de los LEDs como salida
  //pinMode(ledManualPin, OUTPUT);
  //pinMode(ledAutoPin, OUTPUT);

  // Mover los servos a la posición inicial
  servoPan.write(panAngle);
  servoTilt.write(tiltAngle);

  // Apagar los LEDs inicialmente
  //digitalWrite(ledManualPin, LOW);
  //digitalWrite(ledAutoPin, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    switch (command) {
      case 'M':
        ModoManual();
        break;
      case 'S':
        ModoAuto();
        break;
      case 'H':
        Home();
        break;
      case 'Q':
        // Detener todos los modos y esperar otro comando
        return;
    }
  }
}

void ModoManual() {
  while (true) {
    //digitalWrite(ledManualPin, HIGH);
    //delay(10);  // Parpadeo cada 20ms (10ms encendido y 10ms apagado)
    //digitalWrite(ledManualPin, LOW);
    //delay(10);

    if (Serial.available() > 0) {
      char command = Serial.read();
      if (command == 'Q') {
        break;
      } else if (command == 'P' || command == 'T') {
        int value = Serial.parseInt();
        if (command == 'P' && value >= 0 && value <= 180) {
          panAngle = value;
          servoPan.write(panAngle);
        } else if (command == 'T' && value >= 0 && value <= 180) {
          tiltAngle = value;
          servoTilt.write(tiltAngle);
        }
      }
    }
  }
  // Apagar el LED al salir del modo
  //digitalWrite(ledManualPin, LOW);
}

void ModoAuto() {
  while (true) {
    //digitalWrite(ledAutoPin, HIGH);
    //delay(10);  // Parpadeo cada 20ms (10ms encendido y 10ms apagado)
    //digitalWrite(ledAutoPin, LOW);
    //delay(10);

    if (Serial.available() > 0) {
      char command = Serial.read();
      if (command == 'Q') {
        break;
      }
      switch (command) {
        case 'i':
          if (panAngle > 0) {
            panAngle -= 2;
            servoPan.write(panAngle);
          }
          break;
        case 'd':
          if (panAngle < 180) {
            panAngle += 2;
            servoPan.write(panAngle);
          }
          break;
        case 'u':
          if (tiltAngle > 0) {
            tiltAngle += 1;
            servoTilt.write(tiltAngle);
          }
          break;
        case 'b':
          if (tiltAngle < 180) {
            tiltAngle -= 1;
            servoTilt.write(tiltAngle);
          }
          break;
        case 'x':  // Comando para detener los motores
          // No hacer nada, mantener la posición actual
          break;
      }
    }
  }
  // Apagar el LED al salir del modo
  //digitalWrite(ledAutoPin, LOW);
}

void Home() {
  panAngle = 90;
  tiltAngle = 90;
  servoPan.write(panAngle);
  servoTilt.write(tiltAngle);
  delay(2000);
}
