#!/bin/bash

gnome-terminal -- bash -c "./serviceA; exec bash" &
gnome-terminal -- bash -c "sudo ./serviceB; exec bash" &
sleep 2
gnome-terminal -- bash -c "./edge_client; exec bash" &
sleep 2
gnome-terminal -- bash -c "./iot_ide; exec bash" &