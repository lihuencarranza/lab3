import socket
import json
import RPi.GPIO as GPIO
import time
import threading
import sys
import os
import atexit

# Verificar si se está ejecutando como root
if os.geteuid() != 0:
    print("Este script debe ejecutarse como root (sudo)")
    sys.exit(1)

# Configure GPIO
LED_PIN = 26
sockets = []

def cleanup():
    print("\nLimpiando recursos...")
    GPIO.cleanup()
    for sock in sockets:
        try:
            sock.close()
        except:
            pass

# Registrar la función de limpieza
atexit.register(cleanup)

try:
    # Configurar GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    
    # Verificar que el pin está configurado correctamente
    if GPIO.gpio_function(LED_PIN) != GPIO.OUT:
        raise Exception(f"El pin {LED_PIN} no está configurado como salida")
        
except Exception as e:
    print(f"Error al configurar GPIO: {e}")
    sys.exit(1)

# Configure UDP sockets
try:
    humidity_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    humidity_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    humidity_sock.bind(('', 5062))  # Bind to the same port as humidityDetector broadcasts
    humidity_sock.settimeout(1)  # Set 1 second timeout for humidity socket
    sockets.append(humidity_sock)

    command_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    command_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    command_sock.bind(('', 5063))  # New port for command listening
    sockets.append(command_sock)
except Exception as e:
    print(f"Error al configurar sockets: {e}")
    cleanup()
    sys.exit(1)

def handle_humidity():
    try:
        while True:
            try:
                # Receive humidity broadcast with timeout
                data, addr = humidity_sock.recvfrom(1024)
                message = json.loads(data.decode())
                
                if message['type'] == 'humidity':
                    humidity = message['value']
                    
                    # Turn LED on if humidity is below 30%
                    if humidity < 30:
                        GPIO.output(LED_PIN, GPIO.HIGH)
                        print(f"Humidity {humidity}% is low - LED ON")
                        time.sleep(2)  # Keep LED on for 2 seconds
                        GPIO.output(LED_PIN, GPIO.LOW)
                    else:
                        print(f"Humidity {humidity}% is normal - LED OFF")
            except socket.timeout:
                # No humidity data received within timeout
                continue
            except Exception as e:
                print(f"Error in humidity handler: {e}")
                continue
    except Exception as e:
        print(f"Fatal error in humidity handler: {e}")

def handle_commands():
    try:
        print("Esperando comandos en el puerto 5063...")
        while True:
            try:
                # Receive command
                print("Intentando recibir datos...")
                data, addr = command_sock.recvfrom(1024)
                print(f"Recibido datos en el puerto 5063: {data} de {addr}")
                message = json.loads(data.decode())
                print(f"Mensaje decodificado: {message}")
                
                if message['type'] == 'command':
                    command = message['value']
                    print(f"Comando recibido: {command}")
                    if command == 'on':
                        GPIO.output(LED_PIN, GPIO.HIGH)
                        print("Manual command - LED ON")
                    elif command == 'off':
                        GPIO.output(LED_PIN, GPIO.LOW)
                        print("Manual command - LED OFF")
            except socket.timeout:
                print("Timeout esperando comandos...")
                continue
            except Exception as e:
                print(f"Error procesando comando: {e}")
                continue
    except Exception as e:
        print(f"Error fatal en command handler: {e}")

def main():
    try:
        print("Starting LED Service...")
        print("LED control is available on port 5063")
        print("Humidity monitoring is available on port 5062 (optional)")
        
        # Start humidity handler in a separate thread
        humidity_thread = threading.Thread(target=handle_humidity)
        humidity_thread.daemon = True
        humidity_thread.start()
        
        # Start command handler in a separate thread
        command_thread = threading.Thread(target=handle_commands)
        command_thread.daemon = True
        command_thread.start()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
                    
    except KeyboardInterrupt:
        print("\nStopping LED service...")
    finally:
        GPIO.cleanup()
        humidity_sock.close()
        command_sock.close()

def send_command(command):
    try:
        print(f"Intentando enviar comando: {command}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Usar exactamente el mismo formato que netcat
        message = '{"type": "command", "value": "' + command + '"}'
        print(f"Mensaje a enviar: {message}")
        # Enviar el mensaje sin codificar (como netcat)
        sock.sendto(message.encode(), ('127.0.0.1', 5063))
        time.sleep(0.1)  # Dar tiempo para que el mensaje se envíe
        print("Comando enviado exitosamente")
    except Exception as e:
        print(f"Error enviando comando: {e}")
    finally:
        try:
            sock.close()
        except:
            pass
        print("Socket cerrado")

# Usage:
# send_command("on")  # Turn LED on
# send_command("off") # Turn LED off

if __name__ == "__main__":
    main()
