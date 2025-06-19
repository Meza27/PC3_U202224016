# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time

# Parámetros de IP y puerto del robot
ROBOT_IP = "127.0.0.1"
PORT = 58404

tts = ALProxy("ALTextToSpeech", ROBOT_IP, PORT)
motion = ALProxy("ALMotion", ROBOT_IP, PORT)
posture = ALProxy("ALRobotPosture", ROBOT_IP, PORT)
#asr = ALProxy("ALSpeechRecognition", ROBOT_IP, PORT)
memory = ALProxy("ALMemory", ROBOT_IP, PORT)

def escuchar_palabra(asr, memory, nombre_suscripcion, vocabulario, tiempo_espera=4):
    asr.setVocabulary(vocabulario, False)
    asr.subscribe(nombre_suscripcion)
    tiempo_inicio = time.time()
    reconocida = None
    while time.time() - tiempo_inicio < tiempo_espera:
        palabra = memory.getData("WordRecognized")
        if palabra and isinstance(palabra, list) and len(palabra) > 1 and palabra[1] > 0.4:
            reconocida = palabra[0]
            break
        time.sleep(0.1)
    asr.unsubscribe(nombre_suscripcion)
    return reconocida

# Posición inicial
posture.goToPosture("StandInit", 2.0)
tts.setLanguage("Spanish")
tts.say("Hola, soy el asistente de clase.")
time.sleep(1.5)

# --- Simulación de Toma de Asistencia ---
students = ["Andrea", "Carlos", "Luis", "Valeria"]
present_students = []

tts.say("Vamos a tomar la asistencia.")
time.sleep(1.5)

#for name in students:
#    tts.say("¿Está presente " + name + "?")
#    respuesta = escuchar_palabra(asr, memory, "Attendance", ["sí", "no"])
#    if respuesta == "sí":
#        present_students.append(name)
#        # Movimiento: asentir con la cabeza
#        motion.angleInterpolation(["HeadPitch"], [0.2], [0.5], True)
#        motion.angleInterpolation(["HeadPitch"], [0.0], [0.5], True)
#        tts.say(name + " registrado como presente.")
#    else:
#        tts.say("Anotado como ausente.")
#   time.sleep(1)
#
# --- Traducción a alumnos de intercambio ---
#tts.say("¿Hay alumnos de intercambio hoy?")
#respuesta = escuchar_palabra(asr, memory, "ExchangeCheck", ["sí", "no"])
#
#if respuesta == "sí":
#    tts.say("¡Perfecto! Por favor, levanten la mano.")
#else:
#    tts.say("Entendido.")
#time.sleep(2)

# Gira a su izquierda para ver a los alumnos
motion.angleInterpolation(["HeadYaw"], [0.5], [1.0], True)
time.sleep(1)

exchange_languages = ["Inglés", "Francés", "Chino"]

for lang in exchange_languages:
    tts.say("Mostrando traducción al " + lang)
    time.sleep(1)
    if lang == "Inglés":
        tts.setLanguage("English")
        tts.say("Welcome to class! Let's have a great time.")
    elif lang == "Francés":
        tts.setLanguage("French")
        tts.say("Bienvenue en cours! Apprenons ensemble.")
    elif lang == "Chino":
        tts.setLanguage("Chinese")
        tts.say("欢迎来到课堂！让我们一起学习。")
    time.sleep(2)

# Volver al idioma español
tts.setLanguage("Spanish")
motion.angleInterpolation(["HeadYaw"], [0.0], [1.0], True)
time.sleep(1.5)

# --- Preguntas de la clase ---
tts.say("Ahora haré una pregunta de repaso.")
time.sleep(1.5)
tts.say("¿Cuánto es 5 por 3?")

# Levanta la mano
motion.setAngles(["RShoulderPitch", "RElbowRoll"], [0.8, 1.0], 0.2)
time.sleep(1.5)

#respuesta = escuchar_palabra(asr, memory, "Question1", ["quince", "ocho", "nueve"])

# Baja el brazo
motion.setAngles(["RShoulderPitch", "RElbowRoll"], [1.5, 0.0], 0.2)

#if respuesta == "quince":
#    tts.say("¡Correcto! 5 por 3 es 15 porque multiplicamos factores.")
#elif respuesta:
#    tts.say("No es correcto. La respuesta correcta es 15.")
#else:
#    tts.say("No escuché una respuesta clara.")
#time.sleep(2)

# --- Fin de clase ---
tts.say("Gracias por su atención. Esta clase ha terminado.")
time.sleep(1)
tts.say("¡Hasta la próxima!")

# Despedida con cabeza y piernas
motion.angleInterpolation(
    ["HeadPitch", "LHipPitch", "RHipPitch", "LKneePitch", "RKneePitch"],
    [0.3, -0.5, -0.5, 0.6, 0.6],
    [1.0, 1.0, 1.0, 1.0, 1.0],
    True
)
time.sleep(1)

# Volver a posición normal
motion.angleInterpolation(
    ["HeadPitch", "LHipPitch", "RHipPitch", "LKneePitch", "RKneePitch"],
    [0.0, 0.0, 0.0, 0.0, 0.0],
    [1.0, 1.0, 1.0, 1.0, 1.0],
    True
)

motion.setStiffnesses("Body", 0.0)