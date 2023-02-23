# STL Parser
# Tom Geveke
# CAIS Lab, Penn State 2022

class STLParser:
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits import mplot3d
    from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
    import tkinter
    from tkinter import filedialog
    import customtkinter

    def __init__(self, fileName, GUI=True):
        print('STL class __init__()')
        self.open(fileName)
        self.parse()
        if GUI:
            self.createGUI()

    def parse(self):
        self.points = []
        self.triangles = []
        for line in self.lines:
            line = line.strip()
            words = line.split(' ')
            if words[0] == 'vertex':
                x = float(words[1])
                y = float(words[2])
                z = float(words[3].strip())
                self.points.append([x, y, z])
                
    def graph3D(self, forGUI=False, printdir='Z'):
        fig = self.plt.figure()
        plot = self.plt.axes(projection='3d')

        plot.set_xlabel('X')
        plot.set_ylabel('Y')
        plot.set_zlabel('Z')

        if printdir == 'Z':
            xdata = [point[0] for point in self.points]
            ydata = [point[1] for point in self.points]
            zdata = [point[2] for point in self.points]
        elif printdir == 'X':
            xdata = [point[2] for point in self.points]
            ydata = [point[1] for point in self.points]
            zdata = [point[0] for point in self.points]
        plot.scatter3D(xdata, ydata, zdata, c='black')

        index = 0
        for i in range(len(self.points)):
            if index == 3:
                plot.plot(xdata[i-3:i], ydata[i-3:i], zdata[i-3:i], color='gray')
                index = 0
            else:
                index += 1

        if forGUI: 
            return fig
        else: 
            self.plt.show()

    def resize(self, value):
        print('Resize')

    def slice(self):
        print('Slice')
        poses = []
        curheightposes = []
        lastheight = 0
        rowheight = 0.2
        for point in self.points:
            height = point[0]
            if height >= lastheight + rowheight:
                print('New height')
                if curheightposes != []:
                    poses.append(curheightposes)
                    curheightposes = []
            x = point[2]
            y = point[1]
            curheightposes.append([x, y, height])
        return poses
    
    def pose2robot(self, poses):
        bedcenter = [-220, 465, 120]
        bedcenterx = bedcenter[0]
        bedcentery = bedcenter[1]
        bedcenterz = bedcenter[2]
        robposes = []
        for pose in poses:
            print(pose)
            x = pose[0][0]
            print(x)
            print(type(x))
            x = x + bedcenterx
            y = pose[0][1] + bedcentery
            z = pose[0][2] + bedcenterz
            robposes.append([x, y, z])
        return robposes

    def selectPlane(self, value):
        print('Select plane')
        self.fig = self.graph3D(forGUI=True, printdir=value)
        self.updateGraph()

    def updateGraph(self):
        self.fig.clear()
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def open(self, fileName):
        with open(fileName, 'r') as stlFile:
            print('File:', fileName, "opened successfully")
            self.lines = stlFile.readlines()
        self.fileName = fileName
        self.numLines = len(self.lines)
        print('Number of lines =', self.numLines)

    def getFile(self):
        path = self.filedialog.askopenfilename()
        self.open(path)
        print(path)

    def createGUI(self):
        customtkinter = self.customtkinter
        tkinter = self.tkinter
        customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

        self.app = customtkinter.CTk()
        self.app.geometry("800x700")
        self.app.title("STL Slicer")

        self.frame_1 = customtkinter.CTkFrame(master=self.app)
        self.frame_1.pack(pady=20, padx=60, fill="both", expand=True)

        button_openFile = customtkinter.CTkButton(master=self.frame_1, command=self.open, text=self.fileName)
        button_openFile.pack(pady=10, padx=10)

        label_fileName = customtkinter.CTkLabel(master=self.frame_1, justify=tkinter.RIGHT, text="sampleFile.stl")
        label_fileName.pack(pady=10, padx=10)

        label_partView = customtkinter.CTkLabel(master=self.frame_1, justify=tkinter.LEFT, text="Part View")
        label_partView.pack(pady=10, padx=10)

        self.fig = self.graph3D(forGUI=True)

        self.canvas = self.FigureCanvasTkAgg(self.fig, master=self.frame_1)  
        self.canvas.draw()
    
        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().pack()
    
        # creating the Matplotlib toolbar
        toolbar = self.NavigationToolbar2Tk(self.canvas, self.frame_1)
        toolbar.update()
    
        # placing the toolbar on the Tkinter window
        self.canvas.get_tk_widget().pack()

        label_resize = customtkinter.CTkLabel(master=self.frame_1, justify=tkinter.LEFT, text="Resize Part")
        label_resize.pack(pady=10, padx=10)

        slider_resize = customtkinter.CTkSlider(master=self.frame_1, command=self.resize, from_=-1, to=1)
        slider_resize.pack(pady=10, padx=10)
        slider_resize.set(0)

        button_xyzSelect = customtkinter.CTkSegmentedButton(master=self.frame_1, values=["X", "Y", "Z"], command=self.selectPlane)
        button_xyzSelect.pack(pady=10, padx=10)

        button_slice = customtkinter.CTkButton(master=self.frame_1, command=self.slice, text="Slice")
        button_slice.pack(pady=10, padx=10)
        
        button_robot = customtkinter.CTkButton(master=self.frame_1, command=self.slice, text="Execute on Robot")
        button_robot.pack(pady=10, padx=10)

        self.app.mainloop()


if __name__ == "__main__":
    import time
    startTime = time.time()

    obj = STLParser(fileName='TestData/STL/test.stl', GUI=True)
    #poses = obj.slice()
    #robposes = obj.pose2robot(poses)

    totalTime = round(time.time() - startTime, 3)
    print('Runtime =', totalTime, 'seconds')

   # obj.graph3D()
