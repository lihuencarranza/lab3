import socket
import json
import RPi.GPIO as GPIO
import time
import threading
import sys
import os
import atexit

# Check if running as root
if os.geteuid() != 0:
    print("This script must be run as root (sudo)")
    sys.exit(1)

# Configure GPIO
LED_PIN = 26
sockets = []

def cleanup():
    print("\nCleaning up resources...")
    GPIO.cleanup()
    for sock in sockets:
        try:
            sock.close()
        except:
            pass

# Register cleanup function
atexit.register(cleanup)

try:
    # Configure GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    
    # Verify pin is configured correctly
    if GPIO.gpio_function(LED_PIN) != GPIO.OUT:
        raise Exception(f"Pin {LED_PIN} is not configured as output")
        
except Exception as e:
    print(f"Error configuring GPIO: {e}")
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
    print(f"Error configuring sockets: {e}")
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
        print("Waiting for commands on port 5063...")
        while True:
            try:
                # Receive command
                print("Attempting to receive data...")
                data, addr = command_sock.recvfrom(1024)
                print(f"Received data on port 5063: {data} from {addr}")
                message = json.loads(data.decode())
                print(f"Decoded message: {message}")
                
                if message['type'] == 'command':
                    command = message['value']
                    print(f"Command received: {command}")
                    if command == 'on':
                        GPIO.output(LED_PIN, GPIO.HIGH)
                        print("Manual command - LED ON")
                    elif command == 'off':
                        GPIO.output(LED_PIN, GPIO.LOW)
                        print("Manual command - LED OFF")
            except socket.timeout:
                print("Timeout waiting for commands...")
                continue
            except Exception as e:
                print(f"Error processing command: {e}")
                continue
    except Exception as e:
        print(f"Fatal error in command handler: {e}")

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
        print(f"Attempting to send command: {command}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Use exactly the same format as netcat
        message = '{"type": "command", "value": "' + command + '"}'
        print(f"Message to send: {message}")
        # Send message without encoding (like netcat)
        sock.sendto(message.encode(), ('127.0.0.1', 5063))
        time.sleep(0.1)  # Give time for message to be sent
        print("Command sent successfully")
    except Exception as e:
        print(f"Error sending command: {e}")
    finally:
        try:
            sock.close()
        except:
            pass
        print("Socket closed")

# Usage:
# send_command("on")  # Turn LED on
# send_command("off") # Turn LED off

if __name__ == "__main__":
    main()
