from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import json
import threading
import socket
import struct
import logging
from datetime import datetime
import os
import time
import socketio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Initialize Flask and Socket.IO
app = Flask(__name__, 
    static_folder='templates',
    static_url_path='',
    template_folder='templates'
)

# Socket.IO Configuration
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

# Atlas working directory configuration
ATLAS_WORKING_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'atlas_apps')
if not os.path.exists(ATLAS_WORKING_DIR):
    os.makedirs(ATLAS_WORKING_DIR)

# Application state
things = {}
entities = {}  # Dictionary for entities
services = {}
relationships = {}
space_info = {}
apps = {}
runtime_apps = {}  # Dictionary to maintain state of running apps
completed_apps = {}  # Dictionary to maintain history of completed apps

# Multicast configuration
MULTICAST_GROUP = '232.1.1.1'
MULTICAST_PORT = 1235

# Atlas configuration
ATLAS_SERVER_IP = "192.168.8.195"  # Raspberry Pi IP
ATLAS_SERVER_PORT = 6668

# Structure to store app logs
app_logs = {}

def send_tweet_to_atlas(tweet_data):
    """Sends a tweet to Atlas using TCP socket."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            # Connect to Atlas server
            client_socket.connect((ATLAS_SERVER_IP, ATLAS_SERVER_PORT))
            
            # Send tweet
            tweet_json = json.dumps(tweet_data)
            client_socket.sendall(tweet_json.encode('utf-8'))
            
            # Wait for response
            response = client_socket.recv(1024).decode('utf-8')
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"[{current_time}] Server Response: {response}")
            
            return True, response
    except Exception as e:
        logging.error(f"Failed to connect to the server: {e}")
        return False, str(e)

class AppStatus:
    def __init__(self):
        self.status = "stopped"
        self.start_time = None
        self.thread = None
        self.stop_event = threading.Event()
        self.logs = []
        self.app_name = None
        self.app = None
        self.completion_time = None
        self.auto_complete = False  # Indicates if app should auto-complete

    def start(self):
        self.status = "active"
        self.start_time = datetime.now()
        self.stop_event.clear()
        self.logs = []
        self.thread = threading.Thread(target=self.run_app)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        if self.auto_complete:
            self.add_log("Cannot stop app: Auto-completing app")
            return False
        
        self.status = "stopped"
        if self.thread and self.thread.is_alive():
            self.stop_event.set()
            self.thread = None
            self.add_log("App stopped by user")
            # Move app from runtime to completed
            if self.app_name in runtime_apps:
                completed_apps[self.app_name] = self
                runtime_apps.pop(self.app_name)
            with app.app_context():
                socketio.emit('app_status_update', {
                    'app_name': self.app_name,
                    'status': self.status,
                    'action': 'stopped'
                })
            return True
        return False

    def complete(self):
        with app.app_context():
            self.status = "completed"
            self.thread = None
            self.completion_time = datetime.now()
            # Move app from runtime to completed
            if self.app_name in runtime_apps:
                completed_apps[self.app_name] = self
                runtime_apps.pop(self.app_name)
            # Emit updated status
            socketio.emit('app_status_update', {
                'app_name': self.app_name,
                'status': self.status,
                'action': 'completed',
                'success': True,
                'completion_time': self.completion_time.isoformat()
            })

    def add_log(self, message):
        with app.app_context():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] {message}"
            self.logs.append(log_entry)
            # Emit log through Socket.IO
            socketio.emit('app_log', {
                'app_name': self.app_name,
                'log': log_entry,
                'success': True
            })

    def run_app(self):
        try:
            # Wait 5 seconds before starting execution
            self.add_log("Getting ready to run...")
            for i in range(5, 0, -1):
                if self.stop_event.is_set():
                    self.add_log("App execution cancelled by user")
                    return
                time.sleep(1)
            
            self.add_log("Ready for running")
            
            # Send activation tweet to Atlas
            self.add_log("Sending activation tweet to Atlas...")
            
            # Create and send activation tweet for each service
            for service in self.app.get('services', []):
                if self.stop_event.is_set():
                    self.add_log("App execution stopped by user")
                    break
                
                # Get service info from services dictionary
                service_id = service.get('id')
                if service_id in services:
                    service_info = services[service_id]
                    api = service_info.get('api', '')
                    service_name = api.split(':')[0] if api else service_info.get('name', 'Unknown')
                    
                    # Create tweet for service
                    service_tweet = {
                        "Tweet Type": "Service call",
                        "Thing ID": service_info.get('thing_id', 'raspberry1'),
                        "Space ID": service_info.get('space_id', 'MySmartSpace'),
                        "Service Name": service_name,
                        "Service Inputs": "()"
                    }
                    
                    # Send tweet to Atlas
                    success, response = send_tweet_to_atlas(service_tweet)
                    
                    if success:
                        self.add_log(f"Service tweet sent successfully: {service_name}")
                        self.add_log(f"Atlas response: {response}")
                    else:
                        self.add_log(f"Error sending service tweet: {response}")
                    
                    # Simulate execution time
                    time.sleep(2)
                    
                    if self.stop_event.is_set():
                        break
                    
                    self.add_log(f"Service {service_name} completed")
                else:
                    self.add_log(f"Service {service_id} not found in available services")
            
            if not self.stop_event.is_set():
                self.add_log("App execution completed successfully")
                self.complete()
            
        except Exception as e:
            self.add_log(f"Error during app execution: {str(e)}")
            with app.app_context():
                self.status = "error"
                # Move app from runtime to completed with error status
                if self.app_name in runtime_apps:
                    completed_apps[self.app_name] = runtime_apps.pop(self.app_name)
                socketio.emit('app_status_update', {
                    'app_name': self.app_name,
                    'status': self.status,
                    'action': 'error'
                })

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
                    logging.info(f"Processing Identity_Entity tweet for entity {entity_id} from thing {thing_id}")
                    
                    # Store entity information with entity_id as key
                    entities[entity_id] = {
                        "id": entity_id,
                        "name": payload.get("Name", ""),
                        "type": payload.get("Type", ""),
                        "owner": payload.get("Owner", ""),
                        "vendor": payload.get("Vendor", ""),
                        "description": payload.get("Description", ""),
                        "thing_id": thing_id,
                        "space_id": payload.get("Space ID", "")
                    }
                    logging.info(f"Stored entity {entity_id} in entities dictionary. Current entities: {list(entities.keys())}")
                    socketio.emit('entities_update', list(entities.values()), broadcast=True)
                    logging.info(f"Emitted entities_update with {len(entities)} entities")
                
                elif tweet_type == "Service":
                    service_name = payload.get("Name", "")
                    thing_id = payload.get("Thing ID", "")
                    entity_id = payload.get("Entity ID", "")
                    space_id = payload.get("Space ID", "")
                    api = payload.get("API", "")
                    
                    logging.info(f"Processing Service tweet for service {service_name} from entity {entity_id}")
                    
                    # Create a unique service ID combining entity_id and service_name
                    service_id = f"{entity_id}_{service_name}"
                    
                    # Store service information
                    services[service_id] = {
                        "id": service_id,
                        "name": service_name,
                        "api": api,
                        "type": payload.get("Type", ""),
                        "app_category": payload.get("AppCategory", ""),
                        "description": payload.get("Description", ""),
                        "keywords": payload.get("Keywords", ""),
                        "thing_id": thing_id,
                        "entity_id": entity_id,
                        "space_id": space_id,
                        "owner": "N/A",
                        "vendor": "N/A"
                    }
                    logging.info(f"Stored service {service_id} in services dictionary. Current services: {list(services.keys())}")
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

# Application routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/things')
def things_page():
    return render_template('things.html')

@app.route('/entities')
def entities_page():
    return render_template('entities.html')

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

@app.route('/api/entities')
def get_entities():
    return jsonify(list(entities.values()))

@app.route('/api/services')
def get_services():
    return jsonify(list(services.values()))

@app.route('/api/relationships')
def get_relationships():
    return jsonify(list(relationships.values()))

@app.route('/api/space')
def get_space():
    return jsonify(space_info)

@app.route('/api/apps')
def get_apps():
    return jsonify({
        'apps': list(apps.values()),
        'runtime_apps': {
            name: {
                'status': status.status,
                'start_time': status.start_time.isoformat() if status.start_time else None,
                'logs': status.logs,
                'can_activate': status.status in ['stopped', 'completed', 'error'],
                'can_stop': status.status == 'active',
                'success': status.status != 'error'
            } for name, status in runtime_apps.items()
        },
        'completed_apps': {
            name: {
                'status': status.status,
                'start_time': status.start_time.isoformat() if status.start_time else None,
                'completion_time': status.completion_time.isoformat() if status.completion_time else None,
                'logs': status.logs,
                'can_activate': True,
                'can_stop': False,
                'success': status.status != 'error'
            } for name, status in completed_apps.items()
        }
    })

@app.route('/api/apps', methods=['POST'])
def save_app():
    """Saves a new app or updates an existing one."""
    app_data = request.json
    success, message = save_app_to_file(app_data)
    return jsonify({"success": success, "message": message})

@app.route('/api/apps/<app_name>', methods=['DELETE'])
def delete_app(app_name):
    """Deletes an app."""
    success, message = delete_app_file(app_name)
    return jsonify({"success": success, "message": message})

@app.route('/api/apps/<app_name>/activate', methods=['POST'])
def activate_app(app_name):
    if app_name not in apps:
        return jsonify({'success': False, 'message': 'App not found'}), 404
    
    # Check if app is in runtime_apps and not active
    if app_name in runtime_apps:
        app_status = runtime_apps[app_name]
        if app_status.status == 'active':
            return jsonify({'success': False, 'message': 'App is already running'}), 400
        # If app is in runtime_apps but not active, remove it
        runtime_apps.pop(app_name)
    
    try:
        app_status = AppStatus()
        app_status.app_name = app_name
        app_status.app = apps[app_name]
        # Determine if app should auto-complete based on its configuration
        app_status.auto_complete = apps[app_name].get('auto_complete', False)
        runtime_apps[app_name] = app_status
        app_status.start()
        return jsonify({'success': True, 'message': 'App activated successfully'})
    except Exception as e:
        if app_name in runtime_apps:
            del runtime_apps[app_name]
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/apps/<app_name>/stop', methods=['POST'])
def stop_app_endpoint(app_name):
    """Stops an app."""
    if app_name not in runtime_apps:
        return jsonify({"success": False, "message": "App is not running"}), 400
    
    app_status = runtime_apps[app_name]
    if app_status.auto_complete:
        return jsonify({"success": False, "message": "Cannot stop auto-completing app"}), 400
    
    if app_status.stop():
        return jsonify({"success": True, "message": "App stopped successfully"})
    return jsonify({"success": False, "message": "Failed to stop app"}), 500

@app.route('/api/apps/<app_name>/logs')
def get_app_logs(app_name):
    if app_name in runtime_apps:
        return jsonify({
            'success': True,
            'logs': runtime_apps[app_name].logs
        })
    elif app_name in completed_apps:
        return jsonify({
            'success': True,
            'logs': completed_apps[app_name].logs
        })
    return jsonify({
        'success': False,
        'message': 'App not found'
    })

# Socket.IO Events
@socketio.on('connect')
def handle_connect():
    logging.info(f"Client connected: {request.sid}")
    try:
        # Send current data to connecting client
        socketio.emit('things_update', list(things.values()), broadcast=True)
        socketio.emit('entities_update', list(entities.values()), broadcast=True)
        socketio.emit('services_update', list(services.values()), broadcast=True)
        socketio.emit('relationships_update', list(relationships.values()), broadcast=True)
        socketio.emit('space_update', space_info, broadcast=True)
        logging.info("Initial data sent to new client")
    except Exception as e:
        logging.error(f"Error sending initial data: {e}")

@socketio.on('disconnect')
def handle_disconnect():
    logging.info(f"Client disconnected: {request.sid}")

# Start multicast listener in separate thread
multicast_thread = threading.Thread(target=multicast_listener, daemon=True)
multicast_thread.start()
logging.info("Multicast listener started")

def load_apps_from_directory():
    """Loads all apps from working directory."""
    for filename in os.listdir(ATLAS_WORKING_DIR):
        if filename.endswith('.iot'):
            try:
                with open(os.path.join(ATLAS_WORKING_DIR, filename), 'r') as f:
                    app_data = json.load(f)
                    app_name = os.path.splitext(filename)[0]
                    apps[app_name] = app_data
            except Exception as e:
                logging.error(f"Error loading app {filename}: {e}")

def save_app_to_file(app_data):
    """Saves an app to working directory."""
    app_name = app_data.get('name', '').strip()
    if not app_name:
        return False, "App name is required"
    
    # Validate app name
    if not app_name.isalnum():
        return False, "App name must contain only letters and numbers"
    
    filename = f"{app_name}.iot"
    filepath = os.path.join(ATLAS_WORKING_DIR, filename)
    
    try:
        with open(filepath, 'w') as f:
            json.dump(app_data, f, indent=2)
        apps[app_name] = app_data
        return True, "App saved successfully"
    except Exception as e:
        return False, f"Error saving app: {str(e)}"

def delete_app_file(app_name):
    """Deletes an app from working directory."""
    filename = f"{app_name}.iot"
    filepath = os.path.join(ATLAS_WORKING_DIR, filename)
    
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
        if app_name in apps:
            del apps[app_name]
        if app_name in runtime_apps:
            stop_app(app_name)
        return True, "App deleted successfully"
    except Exception as e:
        return False, f"Error deleting app: {str(e)}"

def stop_app(app_name):
    if app_name in runtime_apps:
        runtime_apps[app_name].stop()
        return True
    return False

# Load apps on startup
load_apps_from_directory()

def scan_apps_directory():
    """Scans atlas_apps directory for new and deleted apps."""
    try:
        current_apps = set(apps.keys())
        existing_apps = set()
        
        # Scan directory
        for filename in os.listdir(ATLAS_WORKING_DIR):
            if filename.endswith('.iot'):
                app_name = os.path.splitext(filename)[0]
                existing_apps.add(app_name)
                if app_name not in current_apps:
                    try:
                        with open(os.path.join(ATLAS_WORKING_DIR, filename), 'r') as f:
                            app_data = json.load(f)
                            apps[app_name] = app_data
                            logging.info(f"New app detected: {app_name}")
                            # Notify clients about new app
                            with app.app_context():
                                socketio.emit('new_app_detected', {
                                    'app_name': app_name,
                                    'app_data': app_data
                                })
                    except Exception as e:
                        logging.error(f"Error loading new app {filename}: {e}")
        
        # Detect deleted apps
        deleted_apps = current_apps - existing_apps
        for app_name in deleted_apps:
            if app_name in apps:
                del apps[app_name]
                logging.info(f"App deleted: {app_name}")
                # Notify clients about deleted app
                with app.app_context():
                    socketio.emit('app_deleted', {
                        'app_name': app_name
                    })
    except Exception as e:
        logging.error(f"Error scanning apps directory: {e}")

# Start periodic apps directory scanning
def start_apps_scanner():
    """Starts periodic scanning of apps directory."""
    while True:
        scan_apps_directory()
        time.sleep(5)  # Scan every 5 seconds

# Start apps scanner in separate thread
apps_scanner_thread = threading.Thread(target=start_apps_scanner, daemon=True)
apps_scanner_thread.start()
logging.info("Apps directory scanner started")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False) 