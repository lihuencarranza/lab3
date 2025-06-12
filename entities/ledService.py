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
led_lock = threading.Lock()

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
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    
    # Verify pin is configured correctly
    if GPIO.gpio_function(LED_PIN) != GPIO.OUT:
        raise Exception(f"Pin {LED_PIN} is not configured as output")
    
    # Test LED
    print("Testing LED...")
    GPIO.output(LED_PIN, GPIO.HIGH)
    print("LED should be ON")
    time.sleep(1)
    GPIO.output(LED_PIN, GPIO.LOW)
    print("LED should be OFF")
        
except Exception as e:
    print(f"Error configuring GPIO: {e}")
    sys.exit(1)

# Configure UDP socket for receiving messages
service_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
service_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
MULTICAST_IP = '232.1.1.1'  # Multicast group
MULTICAST_PORT = 6668  # Port for receiving humidity data

# Bind to all interfaces
service_sock.bind(('0.0.0.0', MULTICAST_PORT))

# Join multicast group
mreq = socket.inet_aton(MULTICAST_IP) + socket.inet_aton('0.0.0.0')
service_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def turn_off_led():
    try:
        with led_lock:
            GPIO.setup(LED_PIN, GPIO.OUT) 
            GPIO.output(LED_PIN, GPIO.LOW)
            print("LED turned OFF")
    except Exception as e:
        print(f"Error turning off LED: {e}")
        # Try to reinitialize GPIO
        try:
            GPIO.setup(LED_PIN, GPIO.OUT)
            print("GPIO reinitialized after turn_off error")
        except Exception as e:
            print(f"Error reinitializing GPIO: {e}")

def turn_on_led():
    try:
        with led_lock:
            GPIO.setup(LED_PIN, GPIO.OUT) 
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("LED turned ON")
    except Exception as e:
        print(f"Error turning on LED: {e}")
        # Try to reinitialize GPIO
        try:
            GPIO.setup(LED_PIN, GPIO.OUT)
            print("GPIO reinitialized after turn_on error")
        except Exception as e:
            print(f"Error reinitializing GPIO: {e}")

def handle_messages():
    try:
        while True:
            try:
                # Receive message
                data, addr = service_sock.recvfrom(1024)
                message = json.loads(data.decode())
                
                # Check if it's a humidity data message
                if message.get('Tweet Type') == 'Service_Data':
                    service_name = message.get('Service Name')
                    if service_name == 'Humidity_Service':
                        humidity_data = message.get('Data', {})
                        if humidity_data.get('type') == 'humidity':
                            humidity = humidity_data['value']
                            try:
                                if humidity > 30:
                                    print(f"Humidity {humidity}% is high - LED ON")
                                    turn_on_led()
                                else:
                                    print(f"Humidity {humidity}% is normal - LED OFF")
                                    turn_off_led()
                            except Exception as e:
                                print(f"Error handling humidity: {e}")
                                # Try to reinitialize GPIO
                                try:
                                    GPIO.setup(LED_PIN, GPIO.OUT)
                                    print("GPIO reinitialized after humidity error")
                                except Exception as e:
                                    print(f"Error reinitializing GPIO: {e}")
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error processing message: {e}")
                continue
    except Exception as e:
        print(f"Fatal error in message handler: {e}")

def main():
    try:
        print(f"Listening for messages on port {MULTICAST_PORT}...")
        
        # Start message handler in a separate thread
        message_thread = threading.Thread(target=handle_messages)
        message_thread.daemon = True
        message_thread.start()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
                    
    except KeyboardInterrupt:
        print("\nStopping LED service...")
    finally:
        GPIO.cleanup()
        service_sock.close()

if __name__ == "__main__":
    main()
