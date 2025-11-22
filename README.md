# 🧑‍💻 Projeto IoT — Monitoramento e Automação com Arduino + Python (MediaPipe)

## 🎯 Objetivo

Este projeto integra **Arduino UNO**, **Python** e **MediaPipe** para criar um sistema de detecção e automação física.
A aplicação em Python captura imagens da webcam, processa-as com MediaPipe e envia comandos via porta serial para o Arduino, que controla LEDs, buzzer ou outros atuadores.

O sistema foi projetado para fins educacionais na disciplina Physical Computing – IoT & IoB.

---

## ⚙️ Tecnologias Utilizadas

### 🖥️ Software

- [Python 3.12](https://www.python.org/)
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/guide?hl=pt-br)
- [PySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html)
- [Node-red](https://nodered.org/docs)

### 🔌 Hardware

- [Arduino UNO](https://docs.arduino.cc/hardware/uno-rev3)
- [LEDs](https://docs.arduino.cc/built-in-examples/basics/Blink)
- [Buzzer](https://docs.arduino.cc/libraries/buzzer/#Compatibility)
- [Protoboard](https://docs.arduino.cc/retired/hacking/hardware/building-an-arduino-on-a-breadboard)

---

## 📂 Estrutura do Projeto

```
GS_IoT/
├── GS_IoT.mp4                      # Vídeo explicativo do projeto
├── Hardware_fisico.jpg             # Foto do hardware real montado
├── Hardware_Wokwi.png              # Diagrama do circuito no Wokwi
├── main.py                         # Código Python (MediaPipe + Serial)
├── README.md                       # Documentação original
└── GS_IoT/
    └── GS_IoT.ino                  # Código Arduino para controle físico

```

---

## 🔗 Integração entre os Sistemas

Este projeto funciona como um ecossistema:

### 🖥️ Python (MediaPipe)

- Detecta gestos ou postura usando a webcam
- Envia comandos como “F”, “P”, “C”, “E” para o Arduino via serial
- Pode enviar estado atual para dashboards no futuro

### 🌐 Node-RED

O fluxo importado (flows.json) contém:

- Quatro botões no painel (FOCO, PAUSA, CERTO, ERRADO)
- Cada botão envia uma letra via porta serial para o Arduino
- Usuário pode controlar o pomodoro manualmente pelo navegador

Exemplo do fluxo (simplificado):

- Botão FOCO → envia `F`
- Botão PAUSA → envia `P`
- Botão ERRADO → envia `E`
- Botão CERTO → envia `C`

Todos conectados ao mesmo nó `serial out` que utiliza **COM10** conforme o fluxo

### 🔌 Arduino

- Recebe comandos vindos do Python ou do Node-RED
- Controla LEDs e buzzer
- Cria feedback visual/auditivo do pomodoro

---

## 🚀 Como Executar

1. Clone este repositório:
   ```bash
   git clone https://github.com/JBVJoaoV/GS_IoT.git

2. Acesse o repositório:
   ````bash
   cd GS_IoT
   
3. Instale as dependências:
   ````bash
   pip install opencv-python mediapipe pyserial

4. Configure o Arduino
 
  - Abra o arquivo **GS_IoT.ino** no Arduino IDE.
  - Conecte o Arduino via USB.
  - Selecione a porta correta.
  - Faça o upload.

5. Rodar o Node-RED:
- Instale o Node-RED:
  ````bash
   npm install -g node-red
- Inicie:
  ````bash
   node-red
- Acesse o editor, por meio do link do cmd.
- Importe o arquivo `flows.json`
- Acesse o dashboard, nele haveram 4 botões de status para ser enviados para o arduino.
    


6. Execute o código:
  ````bash
  python main.py
  ````

---

## 🔧 Funcionamento Geral

### 🧠 Python (MediaPipe)

- Captura a imagem da webcam.
- Processa a postura usando MediaPipe.
- Identifica o evento configurado (disparidade na posição dos pontos).
- Envia comandos pela porta serial.
    1- 

### 🔌 Arduino

- Recebe comandos ( `F`, `P`, `E`, `C`)
- Ativa/desativa LEDs, buzzer ou outras ações físicas.
- Retorna dados ao Python quando necessário.

### 🌐 Node-RED

- Oferece controle manual pelo navegador
- Usa o dashboard para enviar os mesmos comandos

---

## 📹 Demonstração

Segue abaixo o link do vídeo de demonstração, caso haja algum problema em acessar, o mesmo se encontra na raiz do projeto.

[Vídeo explicativo](https://drive.google.com/file/d/1ybuOw8Jf4ySRdKAUBqh88TS4kYnsKv6h/view?usp=sharing)

---

## 👾 Prototipo no simulador Wokwi

Segue o link de acesso para o [Wokwi](https://wokwi.com/projects/448251720556221441)

---

## 📌 Limitações

- A performance depende da iluminação e qualidade da webcam.
- O MediaPipe exige boa capacidade de processamento.
- A comunicação serial pode falhar se a porta estiver ocupada.
- O dashboard Node-RED é local.
  
---

## ⏩ Próximos Passos

- Unificar Python e Node-RED para envio simultâneo
- Criar API para envio de métricas
- Dashboard com histórico do pomodoro

---

##   👨‍💻 Integrantes do Projeto

- João Pedro de Souza Vieira Rm: 99805
- Lucas Pisaneschi Speranzini Rm: 98297

---

## 🔒 Nota Ética
Este projeto é 100% educacional e não deve ser utilizado para monitoramento invasivo, automação perigosa ou coleta de imagens sem consentimento.
Respeite sempre normas de segurança elétrica e boas práticas de IoT.
