from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import socket
import json
from datetime import datetime
import threading
import time
import paho.mqtt.client as mqtt
import xmltodict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
socketio = SocketIO(app)

# Global variables to store discovered Atlas services
discovered_things = {}
discovered_services = {}
discovered_relationships = {}

# MQTT Configuration from Atlas_IoTDDL.xml
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPICS = [
    "/Atlas/Network/MQTT_Client",
    "/Atlas/Network/Private_Broker",
    "/Atlas/Multicast/Tweet_ThingIdentity",
    "/Atlas/Multicast/Tweet_EntityIdentity",
    "/Atlas/Multicast/API",
    "/Atlas/Unicast/Interaction"
]

# Multicast Configuration from Atlas_IoTDDL.xml
MULTICAST_IP = "232.1.1.1"
MULTICAST_PORT = 1235

def setup_multicast_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', MULTICAST_PORT))
    
    # Join multicast group
    mreq = socket.inet_aton(MULTICAST_IP) + socket.inet_aton('0.0.0.0')
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    
    return sock

def handle_multicast_message(data):
    """Handle multicast message"""
    try:
        # Parse JSON message
        message = json.loads(data.decode())
        tweet_type = message.get('Tweet Type', '')
        
        # Process based on tweet type
        if tweet_type == 'Identity_Thing':
            handle_thing_identity(message)
        elif tweet_type == 'Identity_Entity':
            handle_entity_identity(message)
        elif tweet_type == 'Service':
            handle_api_message(message)
        elif tweet_type == 'Identity_Language':
            # Skip language identity messages for now
            pass
        else:
            logger.warning(f"Unknown tweet type: {tweet_type}")
            
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON message: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing multicast message: {str(e)}")

def multicast_listener():
    sock = setup_multicast_socket()
    logger.info(f"Listening for multicast messages on {MULTICAST_IP}:{MULTICAST_PORT}")
    
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            logger.info(f"Received multicast data from {addr}")
            handle_multicast_message(data)
        except Exception as e:
            logger.error(f"Error in multicast listener: {e}")

def on_mqtt_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker successfully")
        for topic in MQTT_TOPICS:
            client.subscribe(topic)
            logger.info(f"Subscribed to topic: {topic}")
    else:
        logger.error(f"Failed to connect to MQTT broker with code: {rc}")

def on_mqtt_message(client, userdata, msg):
    try:
        logger.info(f"Received MQTT message on topic {msg.topic}")
        payload = json.loads(msg.payload.decode())
        logger.info(f"Message payload: {payload}")
        
        # Process things first
        if msg.topic == "/Atlas/Multicast/Tweet_ThingIdentity":
            handle_thing_identity(payload)
        elif msg.topic == "/Atlas/Multicast/Tweet_EntityIdentity":
            handle_entity_identity(payload)
            
        # Then process services
        elif msg.topic == "/Atlas/Multicast/API":
            handle_api_message(payload)
        elif msg.topic == "/Atlas/Unicast/Interaction":
            handle_interaction(payload)
            
        # Emit updates to connected web clients
        socketio.emit('update', {
            'things': list(discovered_things.values()),
            'services': list(discovered_services.values()),
            'relationships': list(discovered_relationships.values())
        })
    except Exception as e:
        logger.error(f"Error processing MQTT message: {e}")

def handle_thing_identity(payload):
    thing_id = payload.get('Thing ID')
    if thing_id:
        logger.info(f"Processing thing identity: {thing_id}")
        discovered_things[thing_id] = {
            'id': thing_id,
            'name': payload.get('Name', ''),
            'model': payload.get('Model', ''),
            'vendor': payload.get('Vendor', ''),
            'owner': payload.get('Owner', ''),
            'description': payload.get('Description', ''),
            'os': payload.get('OS', ''),
            'space_id': payload.get('Space ID', ''),
            'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def handle_entity_identity(payload):
    entity_id = payload.get('ID')
    if entity_id:
        logger.info(f"Processing entity identity: {entity_id}")
        thing_id = payload.get('Thing ID')
        if thing_id in discovered_things:
            if 'entities' not in discovered_things[thing_id]:
                discovered_things[thing_id]['entities'] = []
            
            # Check if entity already exists
            entity_exists = False
            for entity in discovered_things[thing_id]['entities']:
                if entity['id'] == entity_id:
                    entity_exists = True
                    break
            
            if not entity_exists:
                discovered_things[thing_id]['entities'].append({
                    'id': entity_id,
                    'name': payload.get('Name', ''),
                    'type': payload.get('Type', ''),
                    'owner': payload.get('Owner', ''),
                    'vendor': payload.get('Vendor', ''),
                    'description': payload.get('Description', '')
                })

def handle_api_message(payload):
    """Handle API message from multicast"""
    try:
        # Extract service information
        service_name = payload.get('Name', '')
        thing_id = payload.get('Thing ID', '')
        entity_id = payload.get('Entity ID', '')
        api_info = payload.get('API', '')
        
        # Generate unique service ID
        service_id = f"{thing_id}_{entity_id}_{service_name}"
        
        # Parse API string
        # Format examples:
        # HumidityDetection:[NULL]:(value,int, NULL)
        # LedControl:["0",int, NULL|"1",int, NULL]:(NULL)
        try:
            # Split API string into parts
            parts = api_info.split(':')
            if len(parts) >= 2:
                # Parse input parameters
                input_params = parts[1].strip('[]').split('|')
                input_types = []
                for param in input_params:
                    if param != 'NULL':
                        # Extract type from parameter
                        type_parts = param.split(',')
                        if len(type_parts) >= 2:
                            input_types.append(type_parts[1].strip())
                
                # Parse output type
                output_type = None
                if len(parts) >= 3:
                    output_parts = parts[2].strip('()').split(',')
                    if len(output_parts) >= 2:
                        output_type = output_parts[1].strip()
        except Exception as e:
            logger.error(f"Error parsing API info: {str(e)}")
            input_types = []
            output_type = None
        
        # Create service object
        service = {
            'id': service_id,
            'name': service_name,
            'thing_id': thing_id,
            'entity_id': entity_id,
            'type': payload.get('Type', ''),
            'description': payload.get('Description', ''),
            'input_types': input_types,
            'output_type': output_type,
            'api_info': api_info,
            'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to services list if not exists
        if not any(s['id'] == service_id for s in discovered_services.values()):
            discovered_services[service_id] = service
            logger.info(f"Added service: {service_name} for entity {entity_id}")
        
    except Exception as e:
        logger.error(f"Error processing API message: {str(e)}")

def handle_interaction(payload):
    relationship_id = payload.get('Relationship_ID')
    if relationship_id:
        logger.info(f"Processing relationship: {relationship_id}")
        discovered_relationships[relationship_id] = {
            'id': relationship_id,
            'source_service': payload.get('Source_Service', ''),
            'target_service': payload.get('Target_Service', ''),
            'type': payload.get('Type', ''),
            'condition': payload.get('Condition', ''),
            'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_mqtt_connect
    client.on_message = on_mqtt_message
    
    try:
        logger.info(f"Connecting to MQTT broker {MQTT_BROKER}:{MQTT_PORT}")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        logger.error(f"Error connecting to MQTT broker: {e}")

def get_space_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return {
        'hostname': hostname,
        'ip_address': ip_address,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'active_things': len(discovered_things),
        'active_services': len(discovered_services),
        'active_relationships': len(discovered_relationships),
        'mqtt_broker': f"{MQTT_BROKER}:{MQTT_PORT}",
        'multicast_group': f"{MULTICAST_IP}:{MULTICAST_PORT}"
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/space-info')
def space_info():
    return jsonify(get_space_info())

@app.route('/api/things')
def get_things():
    return jsonify(list(discovered_things.values()))

@app.route('/api/services')
def get_services():
    services = list(discovered_services.values())
    services.sort(key=lambda x: x['name'])
    return jsonify(services)

@app.route('/api/relationships')
def get_relationships():
    return jsonify(list(discovered_relationships.values()))

if __name__ == '__main__':
    # Start MQTT client in a separate thread
    mqtt_thread = threading.Thread(target=start_mqtt_client)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    
    # Start multicast listener in a separate thread
    multicast_thread = threading.Thread(target=multicast_listener)
    multicast_thread.daemon = True
    multicast_thread.start()
    
    logger.info("Starting Flask application...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True) 