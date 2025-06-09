#!/bin/bash

gnome-terminal -- bash -c "sudo python3 ledService.py; exec bash" &
gnome-terminal -- bash -c "sudo python3 humidityDetector.py; exec bash" &
