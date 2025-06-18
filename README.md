# PC3_U202224016

# Demo Iron NAO - Robot NAO v6

Este proyecto implementa una demostración interactiva en el robot humanoide NAO v6, inspirada en Iron Man. Utiliza control de movimientos, reconocimiento de voz, luces LED y síntesis de voz. El robot puede realizar acciones como escaneo, combate, disparo de rayo repulsor y responder a comandos hablados.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Objetivo de la Implementación
El objetivo de esta implementación es desarrollar una demostración interactiva en el robot humanoide NAO v6, inspirada en el personaje de Iron Man, que combine control de movimiento, reconocimiento de voz, emisión de sonido y efectos visuales mediante LEDs. La demo permite al NAO ejecutar una simulación de una secuencia de acciones predeterminadas (como escaneo del entorno, combate simulado y disparo de rayo repulsor), así como responder a comandos de voz simples. Este trabajo busca demostrar la capacidad de integración de múltiples módulos del robot mediante el uso del lenguaje Python y la arquitectura NAOqi, utilizando primero el simulador Choregraphe para realizar las pruebas respectivas y posteriormente desplegando la demo en el robot físico.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Componentes de la Arquitectura de la Implementación

### 1. Capa de Aplicación (Código Python)
Script Principal: Contiene la lógica de control de la demo, gestionando todo el flujo de acciones. Este código se conecta al robot mediante el uso de proxies (interfaces proporcionadas por la API NAOqi), modificando los parámetros de la IP y el puerto correspondiente.

### 2. Capa de Middleware (NAOqi)
A continuación se mencionan los servicios internos del Robot NAO v6 y cómo se codifican en el script principal:

- ALTextToSpeech: Convierte texto a voz para que el robot hable.
- ALMotion: Permite el control de los motores para mover brazos, cabeza, etc.
- ALRobotPosture: Cambia las posturas generales del cuerpo del NAO.
- ALLeds: Controla el encendido, color e intensidad de los LEDs.
- ALSpeechRecognition: Detecta palabras específicas habladas por el usuario.
    Palabras Clave Reconocidas:
        - `Jarvis`: Activación de diálogo.
        - `armadura`: Activación de luces.
        - `volar`: Animación con brazos extendidos que simula el despegue de vuelo.
        - `despedida`: Finaliza la demo y se despide con una frase típica.
- ALMemory: Sirve como puente de datos entre los eventos detectados (como palabras reconocidas) y el script de Python.

### 3. Capa de Hardware (Robot NAO)
Sensores y Actuadores: Incluyen micrófonos, altavoces, LEDs, motores de movimiento, y sensores internos que ejecutan físicamente las acciones definidas por el software.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

##  Instrucciones de Instalación y Ejecución

### Requisitos previos
Tener instalado Choregraphe (simulador y entorno de desarrollo para NAO).
Tener conexión a la misma red que el robot NAO (para identificar su IP).
Python 2.7 (compatible con la versión de NAOqi SDK usada por Choregraphe).
NAOqi SDK (versión que coincide con la del robot).

### Simulación previa en Choregraphe
1. Abrir Choregraphe y conectar el simulador o el robot real mediante su IP.
2. Abrir el archivo con el script principal en Python.
3. Modificar los parámetros del script para que coincidan con la IP y el puerto del Choreographe.
4. Luego de conectado el robot ya se puede ejecutar el código de Python para su simulación.
5. Verificar que las acciones funcionen correctamente y que en la terminal no aparezca algún error.

### Ejecución en el robot NAO v6
1. Encender el robot y asegurarse de que esté conectado a la red Wi-Fi.
2. Identificar su IP.
3. Conectarse a la misma red Wi-Fi que el robot desde el dispositivo externo.
4. Modificar los parámetros del script con la nueva IP del robot NAO y el puerto correcto.
5. Ejecutar el script. El robot iniciará la demo y responderá a las palabras clave: “Jarvis”, “armadura”, “volar”, “despedida” al momento de iniciar el reconocimiento de voz.
6. Para detener manualmente, se puede presionar Ctrl+C o usar el comando "despedida".