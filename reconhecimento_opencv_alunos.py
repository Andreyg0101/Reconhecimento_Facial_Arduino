import cv2
import os
import numpy as np
import mysql.connector
from datetime import datetime
import serial
import time
import pyttsx3

DATASET_DIR = r"C:\Users\ediso\Videos\projeto_acesso\faces"
PORTA_SERIAL = "COM8"
BAUD_RATE = 9600
LIMIAR_CONFIANCA = 65
voz = pyttsx3.init()

try:
    arduino = serial.Serial(PORTA_SERIAL, BAUD_RATE)
    time.sleep(2)
    print("✅ Serial aberta em", PORTA_SERIAL)
except:
    arduino = None
    print("⚠️ ESP32 não conectado.")

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="controle_acesso"
    )
    cursor = db.cursor()
    print("✅ Conectado ao MySQL.")
except mysql.connector.Error as e:
    print("❌ Erro ao conectar ao banco:", e)
    exit()

print("\n📘 Carregando imagens...")
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

labels, faces, nomes = [], [], []

matricula_fixa = {
    "Andrey Correia Gomes": "UNM0001",
    "Gabriel Belmonte Raimondi": "UNM0002",
    "Lucas Santana de Souza": "UNM0003",
    "Luis Felippe dos Santos Ferreira": "UNM0004",
    "Vinicius Gomes Oliveira Santos": "UNM0005"
}

autorizados = {
    "Andrey Correia Gomes": True,
    "Gabriel Belmonte Raimondi": False,
    "Lucas Santana de Souza": True,
    "Luis Felippe dos Santos Ferreira": False,
    "Vinicius Gomes Oliveira Santos": True
}

label_id = 0
for pessoa in os.listdir(DATASET_DIR):
    pessoa_path = os.path.join(DATASET_DIR, pessoa)
    if not os.path.isdir(pessoa_path):
        continue

    for img_name in os.listdir(pessoa_path):
        img_path = os.path.join(pessoa_path, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        faces_detectadas = detector.detectMultiScale(img)
        for (x, y, w, h) in faces_detectadas:
            faces.append(img[y:y + h, x:x + w])
            labels.append(label_id)
    nomes.append(pessoa)
    label_id += 1

if len(faces) == 0:
    print("❌ Nenhuma imagem encontrada!")
    exit()

recognizer.train(faces, np.array(labels))
print(f"✅ Total de alunos treinados: {len(nomes)}")

camera = cv2.VideoCapture(0)
print("\n📷 Câmera iniciada (pressione 'q' para sair)")

while True:
    ret, frame = camera.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces_detectadas = detector.detectMultiScale(gray, 1.1, 5)

    if len(faces_detectadas) == 0:
        cv2.imshow("Reconhecimento Facial - UNIMES", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    for (x, y, w, h) in faces_detectadas:
        face = gray[y:y + h, x:x + w]
        id_pred, confianca = recognizer.predict(face)

        if confianca < LIMIAR_CONFIANCA and id_pred < len(nomes):
            nome = nomes[id_pred]
            matricula = matricula_fixa.get(nome, "SEM MATRÍCULA")
            autorizado = autorizados.get(nome, False)
            status = "Acesso autorizado" if autorizado else "Acesso negado"
            cor = (0, 255, 0) if autorizado else (0, 0, 255)

            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("SELECT id FROM alunos WHERE matricula = %s", (matricula,))
            existe = cursor.fetchone()

            if existe:
                cursor.execute("""
                    UPDATE alunos
                    SET ultimo_acesso = %s, resultado = %s
                    WHERE matricula = %s
                """, (agora, status, matricula))
            else:
                cursor.execute("""
                    INSERT INTO alunos (nome, matricula, autorizado, ultimo_acesso, resultado)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nome, matricula, autorizado, agora, status))
            db.commit()

            if arduino:
                if autorizado:
                    arduino.write(b'1')
                else:
                    arduino.write(b'0')

            voz.setProperty('rate', 180)
            voz.setProperty('volume', 1.0)
            voz.say(status)
            voz.runAndWait()

        else:
            nome = "Desconhecido"
            cor = (0, 0, 255)
            if arduino:
                arduino.write(b'0')
            voz.say("Acesso negado")
            voz.runAndWait()

        cv2.rectangle(frame, (x, y), (x + w, y + h), cor, 2)
        cv2.putText(frame, f"{nome} ({int(confianca)}%)", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor, 2)

    cv2.imshow("Reconhecimento Facial - UNIMES", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
db.close()
