import socket
import json

# Datos del servidor
IP = '127.0.0.1'
PORT = 6668

# Mensaje de prueba: esto depende del servicio que quieras invocar
# En este caso, vamos a enviar algo gen�rico
mensaje = {
    "Tweet Type": "Service_Request",
    "Thing ID": "RaspberryHumidity",
    "Service": "getHumidity"  # Solo si tu dispositivo ofrece algo llamado as�
}

# Crear socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

# Enviar
client_socket.sendall(json.dumps(mensaje).encode('utf-8'))

# Recibir respuesta
respuesta = client_socket.recv(4096).decode('utf-8')
print("Respuesta del servidor:", respuesta)

# Cerrar socket
client_socket.close()
