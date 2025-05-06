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

## How to run it

After building the executable files, we need to run the .sh file. For that we have to make it executable:

```bash
chmod +x run_all.sh
```

Then run it:

```bash
./run_all.sh
```

This will open three terminals. One for each service and another one for the edge_client.


## How It Works

### Service A (Humidity Sensor Reader)

- Uses SPI to communicate with MCP3008 ADC.
- Reads from channel 0.
- Waits for client (edge client) to connect via TCP on port 5000.
- Sends the raw ADC humidity value to the client.

### Edge Client (Decision Maker)

- Connects to Service A and requests humidity data.
- Converts the ADC value to voltage.
- If the raw value is < 30, sends "ON" to Service B via TCP on port 5001.

### Service B (LED Controller)

- Listens on TCP port 5001.
- Uses libgpiod to control GPIO pin 26.
- When it receives "ON", turns on the LED for 2 seconds.
