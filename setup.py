from os import system

# Install Python dependancies using Pip
system('pip install numpy')
system('pip install matplotlib')
system('pip install Printrun')
system('pip install pyrealsense2')
system('pip install opencv-python')
system('pip install keyboard')

# Download Python SDK for uFactory XArm
system('git clone https://github.com/xArm-Developer/xArm-Python-SDK.git')

