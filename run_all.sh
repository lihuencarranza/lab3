#!/bin/bash

gnome-terminal -- bash -c "./serviceA; exec bash" &
gnome-terminal -- bash -c "sudo ./serviceB; exec bash" &
gnome-terminal -- bash -c "./edge_client; exec bash" &
