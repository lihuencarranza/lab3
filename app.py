from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import json
import threading
import socket
import struct
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Inicializar Flask y Socket.IO
app = Flask(__name__, 
    static_folder='templates',
    static_url_path='',
    template_folder='templates'
)

# Configuración de Socket.IO
socketio = SocketIO(app, 
    cors_allowed_origins="*",
    async_mode='threading',
    logger=True,
    engineio_logger=True,
    ping_timeout=60,
    ping_interval=25,
    max_http_buffer_size=1e8,
    path='/socket.io',
    transports=['polling', 'websocket']
)

# Estado de la aplicación
things = {}
services = {}
relationships = {}
space_info = {}

# Configuración de multicast
MULTICAST_GROUP = '232.1.1.1'
MULTICAST_PORT = 1235

def multicast_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MULTICAST_PORT))
    
    group = socket.inet_aton(MULTICAST_GROUP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    logging.info(f"Listening for multicast messages on {MULTICAST_GROUP}:{MULTICAST_PORT}")
    
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            logging.info(f"Received multicast data from {addr}: {data.decode()}")
            try:
                payload = json.loads(data.decode())
                tweet_type = payload.get("Tweet Type", "")
                
                if tweet_type == "Identity_Thing":
                    thing_id = payload.get("Thing ID", "")
                    things[thing_id] = {
                        "id": thing_id,
                        "name": payload.get("Name", ""),
                        "model": payload.get("Model", ""),
                        "vendor": payload.get("Vendor", ""),
                        "owner": payload.get("Owner", ""),
                        "description": payload.get("Description", ""),
                        "os": payload.get("OS", ""),
                        "space_id": payload.get("Space ID", "")
                    }
                    socketio.emit('things_update', list(things.values()), broadcast=True)
                    logging.info(f"Emitted things_update with {len(things)} things")
                
                elif tweet_type == "Identity_Entity":
                    entity_id = payload.get("ID", "")
                    thing_id = payload.get("Thing ID", "")
                    # Store entity information with entity_id as key
                    services[entity_id] = {
                        "id": entity_id,
                        "name": payload.get("Name", ""),
                        "type": payload.get("Type", ""),
                        "owner": payload.get("Owner", ""),
                        "vendor": payload.get("Vendor", ""),
                        "description": payload.get("Description", ""),
                        "thing_id": thing_id,
                        "space_id": payload.get("Space ID", ""),
                        "api": "N/A",
                        "app_category": "N/A",
                        "keywords": "N/A"
                    }
                    socketio.emit('services_update', list(services.values()), broadcast=True)
                    logging.info(f"Emitted services_update with {len(services)} services")
                
                elif tweet_type == "Service":
                    service_name = payload.get("Name", "")
                    thing_id = payload.get("Thing ID", "")
                    entity_id = payload.get("Entity ID", "")
                    
                    # If we already have an entity with this ID, update its service information
                    if entity_id in services:
                        services[entity_id].update({
                            "api": payload.get("API", ""),
                            "type": payload.get("Type", ""),
                            "app_category": payload.get("AppCategory", ""),
                            "description": payload.get("Description", "") or services[entity_id].get("description", "N/A"),
                            "keywords": payload.get("Keywords", "")
                        })
                    else:
                        # If no entity exists, create a new service entry
                        services[entity_id] = {
                            "id": entity_id,
                            "name": service_name,
                            "api": payload.get("API", ""),
                            "type": payload.get("Type", ""),
                            "app_category": payload.get("AppCategory", ""),
                            "description": payload.get("Description", ""),
                            "keywords": payload.get("Keywords", ""),
                            "thing_id": thing_id,
                            "space_id": payload.get("Space ID", ""),
                            "owner": "N/A",
                            "vendor": "N/A"
                        }
                    
                    socketio.emit('services_update', list(services.values()), broadcast=True)
                    logging.info(f"Emitted services_update with {len(services)} services")
                
                elif tweet_type == "Identity_Language":
                    thing_id = payload.get("Thing ID", "")
                    space_info[thing_id] = {
                        "network_name": payload.get("Network Name", ""),
                        "communication_language": payload.get("Communication Language", ""),
                        "ip": payload.get("IP", ""),
                        "port": payload.get("Port", "")
                    }
                    socketio.emit('space_update', space_info, broadcast=True)
                    logging.info(f"Emitted space_update with info for {thing_id}")
                
            except json.JSONDecodeError as e:
                logging.error(f"Invalid JSON in multicast message: {e}")
        except Exception as e:
            logging.error(f"Error in multicast listener: {e}")

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/things')
def things_page():
    return render_template('things.html')

@app.route('/services')
def services_page():
    return render_template('services.html')

@app.route('/relationships')
def relationships_page():
    return render_template('relationships.html')

@app.route('/apps')
def apps_page():
    return render_template('apps.html')

# API endpoints
@app.route('/api/things')
def get_things():
    return jsonify(list(things.values()))

@app.route('/api/services')
def get_services():
    return jsonify(list(services.values()))

@app.route('/api/relationships')
def get_relationships():
    return jsonify(list(relationships.values()))

@app.route('/api/space')
def get_space():
    return jsonify(space_info)

# Eventos de Socket.IO
@socketio.on('connect')
def handle_connect():
    logging.info(f"Client connected: {request.sid}")
    try:
        # Enviar datos actuales al cliente que se conecta
        socketio.emit('things_update', list(things.values()), broadcast=True)
        socketio.emit('services_update', list(services.values()), broadcast=True)
        socketio.emit('relationships_update', list(relationships.values()), broadcast=True)
        socketio.emit('space_update', space_info, broadcast=True)
        logging.info("Initial data sent to new client")
    except Exception as e:
        logging.error(f"Error sending initial data: {e}")

@socketio.on('disconnect')
def handle_disconnect():
    logging.info(f"Client disconnected: {request.sid}")

# Iniciar el listener de multicast en un hilo separado
multicast_thread = threading.Thread(target=multicast_listener, daemon=True)
multicast_thread.start()
logging.info("Multicast listener started")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False) 