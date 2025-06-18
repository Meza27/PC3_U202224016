# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time

#Parámetros de IP y puerto del robot
ROBOT_IP = "192.168.110.36"
PORT = 9559

tts = ALProxy("ALTextToSpeech", ROBOT_IP, PORT)
motion = ALProxy("ALMotion", ROBOT_IP, PORT)
posture = ALProxy("ALRobotPosture", ROBOT_IP, PORT)
leds = ALProxy("ALLeds", ROBOT_IP, PORT)         
recog = ALProxy("ALSpeechRecognition", ROBOT_IP, PORT) 
memory = ALProxy("ALMemory", ROBOT_IP, PORT)

posture.goToPosture("StandInit", 2.0)

tts.say("Iniciando sistema NAO Stark. Jarvis online.")
time.sleep(1.5)

# Simulación de escaneo con movimiento de cabeza
tts.say("Escaneando el entorno.")
leds.fadeRGB("ChestLeds", 0x0000FF, 1.0) 
for angle in [-0.5, 0.5, 0.0]:
    motion.setAngles("HeadYaw", angle, 0.2)
    time.sleep(1.5)
leds.fadeRGB("ChestLeds", 0xFF0000, 0.5)  

# Posición de combate y simulación de golpes y bloqueos
tts.say("¡Que empiece el combate!")
names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
angles = [0.7, 0.2, -0.8, -0.4]  
motion.setAngles(names, angles, 0.2)
time.sleep(1.5)

# Simula un puñetazo con el brazo derecho 
motion.setAngles(["RShoulderPitch", "RElbowRoll"], [0.7, 0.6], 0.2)
time.sleep(1)
motion.setAngles(["RShoulderPitch", "RElbowRoll"], [1.4, 0.2], 0.2)
time.sleep(1)


# Simula un bloqueo      
motion.setAngles([
    "LShoulderPitch", "RShoulderPitch",
    "LElbowRoll", "RElbowRoll",
    "LElbowYaw", "RElbowYaw"
], [
    0.7, 0.7,
    -1.2, 1.2,
    -0.8, 0.8
], 0.2)
time.sleep(1.5)

posture.goToPosture("StandInit", 2.0)

# Simulación de rayo repulsor
tts.say("¡Rayo repulsor!")
posture.goToPosture("StandInit", 2.0)
motion.setStiffnesses("Body", 1.0)

# Posición estable 
motion.setAngles(["LShoulderPitch", "LElbowYaw", "LElbowRoll"], [0.5, -0.6, -0.4], 0.15)
motion.setAngles(["LHipPitch", "RHipPitch"], [-0.2, -0.2], 0.2)
motion.setAngles("LHand", 1.0, 0.15)
time.sleep(1)
motion.setAngles("LHand", 0.0, 0.15)

posture.goToPosture("StandInit", 2.0)


def despedida():
    tts.say("Yo soy Iron NAO.")
    motion.setAngles("RHand", 1.0, 0.2)
    time.sleep(0.5)
    motion.setAngles("RHand", 0.0, 0.2)

# Configurar el reconocimiento de voz
vocabulary = ["Jarvis", "armadura", "volar", "despedida"]

recog.setLanguage("Spanish")
recog.pause(True) 
recog.setVocabulary(vocabulary, False)
recog.pause(False) 
# Pone al robot en su posición original
motion.setAngles(["LKneePitch", "RKneePitch"], [0.7, 0.7], 0.2)
motion.setAngles(["LHipPitch", "RHipPitch"], [-0.5, -0.5], 0.2)
time.sleep(2)  

recog.subscribe("IronManDemo")  

#Inicio de la función de reconocimiento de voz
tts.say("Reconocimiento de voz activado. Esperando órdenes.")

try:
    while True:
        try:
            word = memory.getData("WordRecognized")
        except RuntimeError:
            word = None
        if word and isinstance(word, list) and len(word) > 1 and word[1] > 0.4:
            recognized_word = word[0]
            print("Palabra reconocida:", recognized_word)
            recog.pause(True)

            #Con la palabra Jarvis, el robot realiza una pregunta
            if recognized_word == "Jarvis":
                tts.say("Sí señor, ¿qué desea que haga?")
                recog.pause(False)
                memory.removeData("WordRecognized")
            #Con la palabra armadura se levanta y prende sus LEDs
            elif recognized_word == "armadura":
                tts.say("Armadura Mark NAO activada")
                posture.goToPosture("StandInit", 2.0)
                leds.fadeRGB("ChestLeds", 0xFF6600, 1.0)
                time.sleep(2)
                recog.pause(False)
                memory.removeData("WordRecognized")
            #Con la palabra volar realiza un movimiento de brazos que simula el inicio de despegue.
            elif recognized_word == "volar":
                tts.say("Encendiendo propulsores.")
                motion.setAngles(["LShoulderPitch", "RShoulderPitch"], [-1.2, -1.2], 0.2)
                motion.setAngles(["LElbowRoll", "RElbowRoll"], [-0.1, 0.1], 0.2)
                motion.setAngles(["LHand", "RHand"], [1.0, 1.0], 0.15)
                time.sleep(2)
                motion.setAngles(["LHand", "RHand"], [0.0, 0.0], 0.15)
                posture.goToPosture("StandInit", 1.0)
                recog.pause(False)
                memory.removeData("WordRecognized")
            #Con la palabra despedida se termina el reconocimiento de voz y se termina la demo.
            elif recognized_word == "despedida":
                despedida()
                recog.pause(False)
                recog.unsubscribe("IronManDemo") 
                break
        time.sleep(0.5)
except KeyboardInterrupt:
    recog.unsubscribe("IronManDemo")
    tts.say("Reconocimiento de voz detenido.")


motion.setStiffnesses("Body", 0.0)
