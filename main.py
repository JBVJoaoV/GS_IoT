import cv2
import mediapipe as mp
import serial
import time

# --------------------------
# CONFIGURAÇÕES DO POMODORO
# --------------------------
Tempo_foco = 10
Tempo_pausa_curta = 2
Tempo_pausa_longa = 5
ciclos = 4

ciclo_atual = 0
pomodoros_completos = 0

estado = "aguardando_inicio"
duracao_atual = 10  # timer inicial de 10s
tempo_inicio_estado = time.time()

# --------------------------
# CONTADOR DE POSTURA
# --------------------------
THRESHOLD_EAR_SHOULDER = 40
THRESHOLD_SHOULDER_HIP = 40

postura_incorreta_total = 0
postura_anterior = "correta"

# --------------------------
# ARDUINO
# --------------------------
arduino = serial.Serial('COM10', 9600)
time.sleep(2)

# --------------------------
# MEDIAPIPE
# --------------------------
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# --------------------------
# CÂMERA
# --------------------------
cap = cv2.VideoCapture(0)

def formatar_tempo(segundos):
    segundos_restantes = int(segundos)
    return f"{segundos_restantes:02}"


# ============================================================
# LOOP PRINCIPAL
# ============================================================
while cap.isOpened():

    success, frame = cap.read()
    if not success:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    # ============================================================
    #  DETECÇÃO DE POSTURA
    # ============================================================
    if results.pose_landmarks:
        h, w, _ = frame.shape
        lm = results.pose_landmarks.landmark

        ear = lm[7]
        shoulder = lm[11]
        hip = lm[23]

        ear_x, ear_y = int(ear.x * w), int(ear.y * h)
        sh_x, sh_y = int(shoulder.x * w), int(shoulder.y * h)
        hip_x, hip_y = int(hip.x * w), int(hip.y * h)

        cv2.circle(frame, (ear_x, ear_y), 7, (0, 255, 255), -1)
        cv2.circle(frame, (sh_x, sh_y), 7, (0, 255, 0), -1)
        cv2.circle(frame, (hip_x, hip_y), 7, (255, 0, 0), -1)
        cv2.line(frame, (ear_x, ear_y), (sh_x, sh_y), (255, 255, 0), 2)
        cv2.line(frame, (sh_x, sh_y), (hip_x, hip_y), (255, 255, 0), 2)

        ear_shoulder_diff = abs(ear_x - sh_x)
        shoulder_hip_diff = abs(sh_x - hip_x)

        if (ear_shoulder_diff < THRESHOLD_EAR_SHOULDER and
            shoulder_hip_diff < THRESHOLD_SHOULDER_HIP):
            postura_atual = "correta"
            texto_postura = "POSTURA CORRETA"
            cor_postura = (0, 255, 0)
        else:
            postura_atual = "incorreta"
            texto_postura = "POSTURA INCORRETA"
            cor_postura = (0, 0, 255)

        # -----------------------------------------------
        #  CONTAGEM SOMENTE NA TRANSIÇÃO CORRETA → INCORRETA
        # -----------------------------------------------
        if postura_anterior == "correta" and postura_atual == "incorreta":
            postura_incorreta_total += 1

            # >>> ARDUINO <<<
            arduino.write(b'E')  # LED vermelho + 2 beeps

        # Se voltou à postura correta → apaga LED vermelho
        if postura_anterior == "incorreta" and postura_atual == "correta":
            arduino.write(b'C')  # apaga LED vermelho

        postura_anterior = postura_atual


    # ============================================================
    #  LÓGICA DO POMODORO
    # ============================================================
    tempo_restante = duracao_atual - (time.time() - tempo_inicio_estado)

    # Timer inicial de 10 segundos
    if estado == "aguardando_inicio":
        cv2.putText(frame, f"Iniciando em: {formatar_tempo(tempo_restante)}",
                    (160, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)

        if tempo_restante <= 0:
            estado = "foco"
            duracao_atual = Tempo_foco
            tempo_inicio_estado = time.time()

            # >>> ARDUINO <<<
            arduino.write(b'F')  # modo foco

    else:
        if tempo_restante <= 0:
            if estado == "foco":
                ciclo_atual += 1

                if ciclo_atual < ciclos:
                    estado = "pausa_curta"
                    duracao_atual = Tempo_pausa_curta

                    # >>> ARDUINO <<<
                    arduino.write(b'P')  # pausa curta

                else:
                    estado = "pausa_longa"
                    duracao_atual = Tempo_pausa_longa
                    pomodoros_completos += 1

                    # >>> ARDUINO <<<
                    arduino.write(b'P')  # pausa longa (verde também)

            elif estado == "pausa_curta" or estado == "pausa_longa":
                estado = "foco"
                duracao_atual = Tempo_foco

                # >>> ARDUINO <<<
                arduino.write(b'F')  # foco novamente

            tempo_inicio_estado = time.time()

        # Exibir informações
        cv2.putText(frame, f"Estado: {estado}",
                    (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
        cv2.putText(frame, f"Tempo: {formatar_tempo(tempo_restante)}s",
                    (10, 340), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
        cv2.putText(frame, f"Ciclo: {ciclo_atual}/{ciclos}",
                    (10, 380), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
        cv2.putText(frame, f"Pomodoros completos: {pomodoros_completos}",
                    (10, 420), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
        cv2.putText(frame, f"Postura incorreta: {postura_incorreta_total}",
                    (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,100,255), 3)
        cv2.putText(frame, texto_postura,
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, cor_postura, 3)

    cv2.imshow("Postura + Pomodoro", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
arduino.close()
cv2.destroyAllWindows()
