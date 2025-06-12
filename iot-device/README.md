# LED Control and Humidity Detector Service

This system consists of two main components:
1. A humidity detector that reads values from the sensor and transmits them via UDP
2. An LED service that can be controlled manually or respond automatically to humidity levels

## Requirements

- Raspberry Pi with Raspbian
- LED connected to GPIO pin 26 (BCM)
- 220Ω resistor in series with the LED
- Humidity sensor connected to MCP3008 (ADC) on channel 0
- Python 3
- netcat (install with `sudo apt-get install netcat-openbsd`)
- spidev (install with `sudo apt-get install python3-spidev`)

## Installation

1. Install dependencies:
```bash
sudo apt-get install netcat-openbsd python3-spidev
```

2. Ensure hardware is connected correctly:
   - LED positive (long side) → GPIO 26
   - LED negative (short side) → GND
   - 220Ω resistor in series with the LED
   - Humidity sensor → MCP3008 channel 0

3. Enable SPI on Raspberry Pi:
```bash
sudo raspi-config
```
Select "Interfacing Options" → "SPI" → "Yes"

## Ports Used

- **Port 5062**: Used by the humidity detector to transmit readings
- **Port 5063**: Used by the LED service to receive manual commands

## Usage

### 1. Start the Humidity Detector

```bash
cd /home/lihuen/Documents/lab3/iot-device
sudo python3 humidityDetector.py
```

You should see messages like:
```
Starting humidity detector...
Broadcasting humidity values on port 5062
Broadcast humidity: XX.X% (Raw: XXX)
```

### 2. Start the LED Service

In another terminal:
```bash
cd /home/lihuen/Documents/lab3/iot-device
sudo python3 ledService.py
```

You should see:
```
Starting LED Service...
LED control is available on port 5063
Humidity monitoring is available on port 5062 (optional)
Waiting for commands on port 5063...
```

### 3. Manual LED Control

In a new terminal, you can send commands using netcat:

To turn on the LED:
```bash
echo -n '{"type": "command", "value": "on"}' | nc -u 127.0.0.1 5063
```

To turn off the LED:
```bash
echo -n '{"type": "command", "value": "off"}' | nc -u 127.0.0.1 5063
```

### 4. Verify Operation

When you send a command, you should see in the LED service terminal:
```
Received data on port 5063: b'{"type": "command", "value": "on"}' from ('127.0.0.1', XXXX)
Decoded message: {'type': 'command', 'value': 'on'}
Command received: on
Manual command - LED ON
```

And the LED should physically turn on/off.

## Automatic Behavior

The system has two modes of operation:

1. **Manual Control**: The LED responds to commands sent to port 5063
2. **Humidity Control**: 
   - The LED turns on automatically if humidity is below 30%
   - Stays on for 2 seconds
   - Manual commands take priority over automatic control

## Troubleshooting

1. If the LED doesn't respond:
   - Check the physical LED connection
   - Make sure the service is running with sudo
   - Verify that ports 5062 and 5063 are not being used by other processes

2. If the humidity detector doesn't work:
   - Verify that SPI is enabled
   - Check the sensor connection to MCP3008
   - Make sure the sensor is on channel 0

3. If commands are not received:
   - Verify that both services are running
   - Make sure the command format is exactly:
     ```json
     {"type": "command", "value": "on"}
     ```
   - Verify that netcat is being used with the -u option (UDP)

4. To stop the services:
   - Press Ctrl+C in each terminal
   - Or use the commands:
     ```bash
     sudo pkill -f "python3 ledService.py"
     sudo pkill -f "python3 humidityDetector.py"
     ```

## Additional Notes

- The LED service can work without the humidity detector
- The humidity detector transmits readings every second
- Humidity values are shown as percentage (0-100%)
- The LED blinks automatically when humidity is low

## Atlas Integration

The system is configured to integrate with the Atlas middleware. To verify that Atlas is working correctly:

1. **Verify Atlas Configuration**:
   - The `Atlas_IoTDDL.xml` file must be in the correct location:
     ```bash
     cd ../atlas/AtlasThingMiddleware_RPI-master/ConfigurationFiles/
     ```
   - Verify that the file contains the correct configuration:
     - Thing_ATID: "raspy-h"
     - Thing_Name: "Humi"
     - Humidity port: 5062
     - LED control port: 5063

2. **Start Services in Order**:
   ```bash
   # 1. Start the humidity detector
   cd ../iot-device
   sudo python3 humidityDetector.py

   # 2. In another terminal, start the LED service
   cd ../iot-device
   sudo python3 ledService.py

   # 3. In a third terminal, start Atlas
   cd ../atlas/AtlasThingMiddleware_RPI-master
   sudo python3 AtlasThingMiddleware.py
   ```

3. **Verify Communication**:
   - Atlas should show messages indicating it has connected to the device
   - You should see device registration messages for "raspy-h"
   - Atlas should show it is receiving humidity readings

4. **Test Functionality**:
   - Verify that Atlas receives humidity readings from port 5062
   - Check that Atlas can send commands to the LED through port 5063
   - Confirm that the LED responds to commands sent by Atlas

5. **Atlas Troubleshooting**:
   - If Atlas doesn't connect:
     - Verify that ports 5062 and 5063 are available
     - Check that the XML configuration file is accessible
     - Make sure services are running with sudo permissions
   
   - If Atlas doesn't receive data:
     - Verify that the humidity detector is transmitting
     - Check that ports match in the configuration
     - Review Atlas logs for specific errors

   - If Atlas can't control the LED:
     - Verify that the LED service is listening for commands
     - Check that the command format is correct
     - Make sure no other processes are using the ports

6. **Restart Services**:
   ```bash
   # Stop all services
   sudo pkill -f "python3 ledService.py"
   sudo pkill -f "python3 humidityDetector.py"
   sudo pkill -f "AtlasThingMiddleware.py"
   
   # Start again in the correct order
   # (Follow steps from point 2)
   ```

- Atlas uses ports 5062 and 5063 to communicate with the system
- The system is configured as "SmartHumiditySystem" in Atlas
- Humidity values are transmitted in real-time to Atlas
- Atlas can control the LED both manually and in response to humidity

### Atlas Tweet Examples

When Atlas is working correctly, you should see different types of tweets in the console. Here are examples of the tweets you should see:

1. **Thing Identity Tweet**:
```json
{
    "Tweet Type": "Identity_Thing",
    "Thing ID": "raspy-h",
    "Space ID": "MySmartSpace",
    "Name": "Humi",
    "Model": "Raspberry Pi 4",
    "Vendor": "Raspberry Pi Foundation",
    "Owner": "Lihuen",
    "Description": "Humidity sensor connected to a Raspberry Pi",
    "OS": "Raspbian"
}
```

2. **Humidity Data Tweet**:
```json
{
    "Tweet Type": "Data",
    "Thing ID": "raspy-h",
    "Service": "Humidity_Service",
    "Value": 45.5,
    "Unit": "percentage",
    "Timestamp": "2024-03-21T10:30:00"
}
```

3. **LED Control Tweet**:
```json
{
    "Tweet Type": "Command",
    "Thing ID": "raspy-h",
    "Service": "LED_Control_Service",
    "Command": "on",
    "Timestamp": "2024-03-21T10:31:00"
}
```

### Tweet Verification

To verify that Atlas is receiving and processing tweets correctly:

1. **Verify identity tweets**:
   - You should see the identity tweet every 20 seconds
   - Confirm that the Thing ID is "raspy-h"
   - Verify that device details are correct

2. **Verify data tweets**:
   - You should see data tweets whenever the humidity sensor sends a reading
   - Values should be between 0 and 100
   - The timestamp should be current

3. **Verify control tweets**:
   - When you send a command to the LED, you should see a control tweet
   - The command should be "on" or "off"
   - The service should be "LED_Control_Service"

### Tweet Troubleshooting

If you don't see the tweets:

1. **Check network configuration**:
   - Make sure ports 5062 and 5063 are open
   - Verify that no firewalls are blocking communication

2. **Verify message format**:
   - Humidity messages must be valid JSON
   - Format must match what Atlas expects

3. **Check logs**:
   - Review Atlas logs for connection errors
   - Verify that services are sending data in the correct format

4. **Restart services**:
   ```bash
   # Stop all services
   sudo pkill -f "python3 ledService.py"
   sudo pkill -f "python3 humidityDetector.py"
   sudo pkill -f "AtlasThingMiddleware.py"
   
   # Start again in the correct order
   # (Follow steps from "Start Services in Order" section)
   ```

## Additional Notes

- The LED service can work without the humidity detector
- The humidity detector transmits readings every second
- Humidity values are shown as percentage (0-100%)
- The LED blinks automatically when humidity is low

### Atlas Recompilation

After modifying the `Atlas_IoTDDL.xml` file, it's necessary to recompile Atlas:

1. **Stop all services**:
```bash
sudo pkill -f "python3 ledService.py"
sudo pkill -f "python3 humidityDetector.py"
sudo pkill -f "AtlasThingMiddleware.py"
```

2. **Recompile Atlas**:
```bash
cd ../atlas/AtlasThingMiddleware_RPI-master
sudo python3 setup.py build
sudo python3 setup.py install
```

3. **Start services in order**:
```bash
# Terminal 1
cd ../iot-device
sudo python3 humidityDetector.py

# Terminal 2
cd ../iot-device
sudo python3 ledService.py

# Terminal 3
cd ../atlas/AtlasThingMiddleware_RPI-master
sudo python3 AtlasThingMiddleware.py
```

4. **Verify compilation**:
   - Atlas should start without errors
   - You should see identity tweets every 20 seconds
   - Tweets should reflect the new XML configuration 