import socket
import time
import json
import spidev
import RPi.GPIO as GPIO

# Configure SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0
spi.max_speed_hz = 1350000

# Configure broadcast socket
broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
BROADCAST_PORT = 5062

def read_humidity():
    # Read from MCP3008 channel 0
    adc_channel = 0
    cmd = 0x18 | (adc_channel & 0x07)
    resp = spi.xfer2([cmd, 0x00, 0x00])
    value = ((resp[1] & 0x03) << 8) | resp[2]
    return value

def main():
    try:
        while True:
            # Read humidity value
            humidity = read_humidity()
            
            # Create message
            message = {
                "type": "humidity",
                "value": humidity,
                "timestamp": time.time()
            }
            
            # Broadcast message
            broadcast_socket.sendto(
                json.dumps(message).encode(),
                ('<broadcast>', BROADCAST_PORT)
            )
            
            print(f"Broadcast humidity: {humidity}")
            time.sleep(1)  # Read every second
            
    except KeyboardInterrupt:
        print("\nStopping humidity detector...")
    finally:
        spi.close()
        broadcast_socket.close()

if __name__ == "__main__":
    main()

