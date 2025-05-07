import socket
import json

# Datos del servidor
IP = '127.0.0.1'
PORT = 7000  # Changed from 6668 to 7000 to match edge client's command port

# Mensaje en el formato que espera el edge client
mensaje = "READ RPi-1 Read_Humidity"

# Crear socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

# Enviar
client_socket.sendall(mensaje.encode('utf-8'))

# Recibir respuesta
respuesta = client_socket.recv(4096).decode('utf-8')
print("Respuesta del servidor:", respuesta)

# Cerrar socket
client_socket.close()
