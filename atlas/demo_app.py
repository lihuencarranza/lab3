import socket
import json

# Configuration
THING_IP = '127.0.0.1'  # Localhost since we're running on the same machine
PORT = 6668  # Default Atlas middleware port

# Service call parameters
service_call = {
    "Tweet Type": "Service call",
    "Thing ID": "RaspberryHumidity",
    "Space ID": "MySmartSpace",
    "Service Name": "getHumidity",
    "Service Inputs": "()"
}

def main():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the Atlas middleware
        print(f"Connecting to Atlas middleware at {THING_IP}:{PORT}...")
        client_socket.connect((THING_IP, PORT))
        
        # Convert service call to JSON string
        json_call = json.dumps(service_call)
        print(f"\nSending service call:\n{json_call}")
        
        # Send the service call
        client_socket.sendall(json_call.encode('utf-8'))
        
        # Receive the response
        response = client_socket.recv(4096).decode('utf-8')
        print(f"\nReceived response:\n{response}")
        
    except ConnectionRefusedError:
        print("Error: Could not connect to Atlas middleware. Make sure it's running.")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main() 