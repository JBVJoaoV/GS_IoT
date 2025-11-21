#define LED_r 13   // LED vermelho
#define LED_g 12   // LED verde
#define LED_y 11   // LED amarelo
#define buzzer 10  // buzzer

void beep(int vezes, int duracao = 150) {
  for (int i = 0; i < vezes; i++) {
    digitalWrite(buzzer, HIGH);
    delay(duracao);
    digitalWrite(buzzer, LOW);
    delay(120);
  }
}

void setup() {
  // Inicialização
  pinMode(LED_r, OUTPUT);
  pinMode(LED_g, OUTPUT);
  pinMode(LED_y, OUTPUT);
  pinMode(buzzer, OUTPUT);

  digitalWrite(LED_r, LOW);
  digitalWrite(LED_g, LOW);
  digitalWrite(LED_y, LOW);
  digitalWrite(buzzer, LOW);

  // *** IMPORTANTE ***
  Serial.begin(9600);   // <-- Faltava isto!
}

void loop() {
  if (Serial.available() > 0) {
    char c = Serial.read();

    if (c == 'F') {
      digitalWrite(LED_y, HIGH);   // LED amarelo
      digitalWrite(LED_g, LOW);
      beep(1);
      Serial.println("Modo FOCUS (Amarelo)");
    }
    else if (c == 'P') {
      digitalWrite(LED_g, HIGH);   // LED verde
      digitalWrite(LED_y, LOW);
      beep(1);
      Serial.println("Modo PAUSA (Verde)");
    }
    else if (c == 'E') {
      digitalWrite(LED_r, HIGH);   // LED vermelho
      beep(2);
      Serial.println("MODO ERRO (Vermelho)");
    }
    else if (c == 'C') {
      digitalWrite(LED_r, LOW);
    }
  }

  delay(10);
}
