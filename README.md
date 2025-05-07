# Lab 3 - Build Microservices for your Smart Space

## Overview

This project demonstrates a simple IoT application using **two services** (Service A and Service B) and an **edge client** running on a single Raspberry Pi. It simulates an environment where:

- **Service A** reads data from a humidity sensor via SPI.
- **Service B** controls an LED using GPIO.
- **Edge Client** coordinates the system:
  - It requests humidity readings from Service A.
  - If the humidity is below 30%, it sends a command to Service B to turn the LED on for 2 seconds.

This architecture illustrates both:

- **Order-based relationship**: Service B only acts after Service A completes its measurement.
- **Condition-based relationship**: The action of Service B is conditional on the value from Service A.

---

All components communicate via **TCP sockets** using `localhost` or fixed IPs if distributed.

## Requirements

- Raspberry Pi (with SPI and GPIO enabled)
- Breadboard + Humidity sensor connected via MCP3008 (SPI ADC)
- LED connected to GPIO26
- `libgpiod` installed
- `tmux` installed for terminal multiplexing

Install dependencies:

```bash
sudo apt update
sudo apt install libgpiod-dev gnome-terminal
```

Enable SPI and GPIO via raspi-config if not already enabled:

```bash
sudo raspiconfig
# Interfaces -> Enable SPI
# Interfaces -> Enable GPIO (usually already enabled)
```

## Compilation

```bash
make all
```

This builds:

* `serviceA` -> reads humidity via SPI
* `serviceB` -> controls LED via GPIO
* `edge_client` -> central controller
* `iot_ide` -> ide

## How to run it

After building the executable files, we need to run the .sh file. For that we have to make it executable:

```bash
chmod +x run_all.sh
```

Then run it:

```bash
./run_all.sh
```

This will open three terminals. One for each service, another one for the edge_client and one for the ide.

## How It Works


### Service Registration

- Each RPi registers its available services by connecting to the edge device on port 6000.
- Example:
  - Sensor registers: (RPi-1, Read_Humidity, 0, -)
  - Actuator registers: (RPi-2, Set_LED, 1, ON/OFF)

### Edge Device Behavior

- Listens for service registrations on port 6000.

- Periodically reads humidity from the sensor (port 5000).

- If humidity < 30, it sends an ON command to the actuator (port 5001), else OFF.

- Listens for user commands from the IDE on port 7000.

### IDE (Interactive Environment)

- Connects to the edge device on port 7000.
- Sends commands like:

  - READ RPi-1 Read_Humidity
  - WRITE RPi-2 Set_LED ON
  - WRITE RPi-2 Set_LED OFF

- The edge device interprets the command and responds with the result.
