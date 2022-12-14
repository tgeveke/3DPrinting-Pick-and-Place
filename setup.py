from os import system
import platform # For determining Windows or Linux

# Install Python dependancies using Pip
system('pip install numpy')
system('pip install matplotlib')
system('pip install Printrun')
system('pip install pyrealsense2')
system('pip uninstall opencv-python')
system('pip install opencv-python')
system('pip install keyboard')
system('pip install -Iv pyserial==3.4') # For connecting to xArm 

# Install customtkinter for stl slicer GUI    
system('pip install customtkinter')

# Download roboflow package for machine learning model
system('pip install roboflow')

''' Deleted since I included xarm directory in my GitHub repository
# Download Python SDK for uFactory XArm
system('git clone https://github.com/xArm-Developer/xArm-Python-SDK.git')
system('cd xArm-Python-SDK')
if platform.system() == 'Windows':
    system('move xarm ../')
    system('cd ../')
    system('rmdir /s xArm-Python-SDK')
elif platform.system() == 'Linux':
    system('mv xarm ../')
    system('cd ../')    
    system('rm -r xArm-Python-SDK')
'''
