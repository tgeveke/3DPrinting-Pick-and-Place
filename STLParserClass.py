# STL Parser
# Tom Geveke
# CAIS Lab, Penn State 2022

class STLParser:
    import numpy as np
    import matplotlib.pyplot as plt

    def __init__(self, fileName, allPoints = False, maxRuns = 100000):
        print('GCodeParser class __init__()')
        with open(fileName, 'r') as stlFile:
            print('File:', fileName, "opened successfully")
            self.lines = stlFile.readlines()
        self.fileName = fileName
        self.numLines = len(self.lines)
        print('Number of lines =', self.numLines)
        if allPoints: self.maxRuns = self.numLines
        else: self.maxRuns = maxRuns
        self.parse()

    def parse(self):
        print('Parsing file for entries =', self.maxRuns)
        self.points = []
        index = 0
        z = 0

        for i in range(self.maxRuns):
            line = self.lines[i].strip()
            words = line.split(' ')
            if words[0] == 'vertex':
                x = float(words[1])
                y = float(words[2])
                z = float(words[3].strip())
                self.points.append([x, y, z])
                
    def graph3D(self):
        from mpl_toolkits import mplot3d
        fig = self.plt.figure()
        plot = self.plt.axes(projection='3d')

        plot.set_xlabel('X')
        plot.set_ylabel('Y')
        plot.set_zlabel('Z')

        xdata = [point[0] for point in self.points]
        ydata = [point[1] for point in self.points]
        zdata = [point[2] for point in self.points]
        
        plot.scatter3D(xdata, ydata, zdata, c='blue')

        index = 0
        for i in range(len(self.points)):
            if index == 3:
                plot.plot(xdata[i-3:i], ydata[i-3:i], zdata[i-3:i], color='lightblue')
                index = 0
            else:
                index += 1

        self.plt.show()

   


if __name__ == "__main__":
    import time
    startTime = time.time()

    obj = STLParser(fileName='TestData/STL/test.stl', allPoints=True)
    totalTime = round(time.time() - startTime, 3)
    print('Runtime =', totalTime, 'seconds')

    obj.graph3D()
