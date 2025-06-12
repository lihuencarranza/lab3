import socket
import time
import json
import spidev
import RPi.GPIO as GPIO
import threading

# Configure SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0
spi.max_speed_hz = 1350000

# Configure broadcast socket
broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
MULTICAST_IP = '232.1.1.1'  # Multicast group
MULTICAST_PORT = 6668  # Atlas's listening port

# Configure command listener socket
command_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
command_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
COMMAND_PORT = 6669  # Port for receiving commands

# Join multicast group
broadcast_socket.bind(('', MULTICAST_PORT))
mreq = socket.inet_aton(MULTICAST_IP) + socket.inet_aton('0.0.0.0')
broadcast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Bind command socket
command_socket.bind(('', COMMAND_PORT))

def read_humidity():
    # Read from MCP3008 channel 0
    adc_channel = 0
    cmd = 0x18 | (adc_channel & 0x07)
    resp = spi.xfer2([cmd, 0x00, 0x00])
    value = ((resp[1] & 0x03) << 8) | resp[2]
    return value

def convert_to_percentage(raw_value):
    """
    Convert raw ADC value (0-1023) to humidity percentage (0-100%)
    The sensor typically outputs:
    - 0-1023 for 0-100% humidity
    - We'll add some basic calibration
    """
    # Ensure the value is within valid range
    raw_value = max(0, min(1023, raw_value))
    
    # Convert to percentage
    percentage = (raw_value / 1023.0) * 100.0
    
    # Round to 1 decimal place
    return round(percentage, 1)

def get_humidity():
    """
    Simple function to get current humidity value
    Returns the humidity percentage
    """
    raw_value = read_humidity()
    return convert_to_percentage(raw_value)

def get_humidity_raw():
    """
    Simple function to get current raw humidity value
    Returns the raw ADC value (0-1023)
    """
    return read_humidity()

def handle_commands():
    while True:
        try:
            data, addr = command_socket.recvfrom(1024)
            command = data.decode().strip()
            
            if command == "GET_HUMIDITY":
                # Read current humidity
                raw_humidity = read_humidity()
                humidity_percentage = convert_to_percentage(raw_humidity)
                
                # Create response message
                response = {
                    "type": "humidity_response",
                    "value": humidity_percentage,
                    "raw_value": raw_humidity
                }
                
                # Send response back to the requester
                command_socket.sendto(json.dumps(response).encode(), addr)
                print(f"Sent humidity response to {addr}: {humidity_percentage}%")
                
        except Exception as e:
            print(f"Error handling command: {e}")

def main():
    try:
        print("Starting humidity detector...")
        print(f"Sending humidity values to multicast group {MULTICAST_IP}:{MULTICAST_PORT}")
        print(f"Listening for commands on port {COMMAND_PORT}")
        
        # Start command handler thread
        command_thread = threading.Thread(target=handle_commands)
        command_thread.daemon = True
        command_thread.start()
        
        while True:
            # Read raw humidity value
            raw_humidity = read_humidity()
            
            # Convert to percentage
            humidity_percentage = convert_to_percentage(raw_humidity)
            
            # Create message in Atlas tweet format
            message = {
                "Tweet Type": "Service_Data",
                "Thing ID": "raspy-h",
                "Space ID": "MySmartSpace",
                "Service Name": "Humidity_Service",
                "Network Name": "MySpaceNetwork",
                "Communication Language": "UDP",
                "IP": "0.0.0.0",
                "Port": "6668",
                "Data": {
                    "type": "humidity",
                    "value": humidity_percentage
                }
            }
            
            # Send message to multicast group
            broadcast_socket.sendto(
                json.dumps(message).encode(),
                (MULTICAST_IP, MULTICAST_PORT)
            )
            
            print(f"Sent humidity: {humidity_percentage}% (Raw: {raw_humidity})")
            time.sleep(5)  # Read every 5 seconds
            
    except KeyboardInterrupt:
        print("\nStopping humidity detector...")
    finally:
        spi.close()
        broadcast_socket.close()
        command_socket.close()

if __name__ == "__main__":
    main()

