#!/bin/bash

# Run Cloud
gnome-terminal -- bash -c "python3 cloud.py; exec bash"

# Run Cloudlets
gnome-terminal -- bash -c "python3 cloudlet1.py; exec bash"
gnome-terminal -- bash -c "python3 cloudlet2.py; exec bash"

# Run Fog nodes
gnome-terminal -- bash -c "python3 fog1.py; exec bash"
gnome-terminal -- bash -c "python3 fog2.py; exec bash"
gnome-terminal -- bash -c "python3 fog3.py; exec bash"
gnome-terminal -- bash -c "python3 fog4.py; exec bash"
