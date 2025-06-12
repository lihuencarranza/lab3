# IoT Device Services

This directory contains the services for the IoT device, including the LED control service and humidity detector.

## LED Service

The LED service (`ledService.py`) controls an LED based on humidity data. It listens on port 6668 for humidity data from the humidity detector.

### Features
- Controls an LED connected to GPIO pin 26
- Responds to humidity data from the humidity detector
- Automatically turns LED on/off based on humidity levels

### Behavior
**Humidity Control**:
- When humidity > 30%: LED turns ON
- When humidity ≤ 30%: LED turns OFF

### Requirements
- Python 3
- RPi.GPIO library
- Root privileges (sudo) for GPIO access

### Usage
1. Run the service with sudo:
```bash
sudo python3 ledService.py
```

2. The service will:
   - Initialize GPIO and test the LED
   - Listen for messages on port 6668
   - Respond to humidity data

### Message Format
The service expects messages in the following format:

For humidity data:
```json
{
    "Tweet Type": "Service_Data",
    "Service Name": "Humidity_Service",
    "Data": {
        "type": "humidity",
        "value": <humidity_value>
    }
}
```

## Humidity Detector

The humidity detector (`humidityDetector.py`) reads humidity data from a sensor and sends it to the LED service.

### Features
- Reads humidity data from a sensor
- Sends data to the LED service via UDP multicast
- Listens for commands on port 6669

### Usage
1. Run the detector:
```bash
sudo python3 humidityDetector.py
```

2. The detector will:
   - Read humidity data from the sensor
   - Send data to multicast group 232.1.1.1:6668
   - Listen for commands on port 6669

### Message Format
The detector sends messages in the following format:
```json
{
    "Tweet Type": "Service_Data",
    "Service Name": "Humidity_Service",
    "Data": {
        "type": "humidity",
        "value": <humidity_value>
    }
}
```

## Network Configuration
- LED Service listens on port 6668
- Humidity Detector sends data to multicast group 232.1.1.1:6668
- Humidity Detector listens for commands on port 6669

## Error Handling
Both services include error handling for:
- GPIO initialization and control
- Network communication
- Message parsing
- Sensor data reading

## Cleanup
Both services properly clean up resources on exit:
- GPIO pins are reset
- Network sockets are closed
- Threads are terminated

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