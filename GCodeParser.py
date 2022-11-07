# G Code Parser
# Tom Geveke
# CAIS Lab, Penn State 2022

class GCodeParser:
    import numpy as np
    import matplotlib.pyplot as plt

    def __init__(self, fileName, allPoints = False, maxRuns = 100000):
        print('GCodeParser class __init__()')
        with open(fileName, 'r') as gcodeFile:
            print('File:', fileName, "opened successfully")
            self.lines = gcodeFile.readlines()
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
            line = self.lines[i]
            words = line.split(' ')
            if words[0] == 'G1':
                if index < self.maxRuns:
                    index += 1
                    for word in words[1:]:
                        firstLetter = word[0]
                        if firstLetter == 'X':
                            try:
                                x = float(word[1:])
                            except:
                                continue
                        elif firstLetter == 'Y':
                            y = float(word[1:])
                        elif firstLetter == 'Z':
                            z = float(word[1:])
                            lastZ = z
                if 'z' not in locals():
                    z = lastZ
                if 'x' in locals() and 'y' in locals():
                    self.points.append([x, y, z])

    def averageXYZ(self, precision = 3):
        if self.points is not None:
            print('Getting average (x, y, z)')
            avgX = round(sum(self.allX) / len(self.allX), precision)
            avgY = round(sum(self.allY) / len(self.allY), precision)
            avgZ = round(sum(self.allZ) / len(self.allZ), precision)
            return (avgX, avgY, avgZ)

    def graph3D(self):  
        from mpl_toolkits import mplot3d
                
        fig = self.plt.figure()
        plot = self.plt.axes(projection='3d')
        
        xdata = [point[0] for point in self.points]
        ydata = [point[1] for point in self.points]
        zdata = [point[2] for point in self.points]
        
        plot.set_xlabel('X')
        plot.set_xlim(0, 250)
        plot.set_ylabel('Y')
        plot.set_ylim(0, 250)
        plot.set_zlabel('Z')
        plot.set_zlim(0, 250)
        
        plot.scatter3D(xdata, ydata, zdata, c=zdata, cmap='prism');
        self.plt.show()
    
    def cluster2D(self, numPoints = 12000, thresh = 25):
        import scipy.cluster.hierarchy as hcluster

        xdata = [point[0] for point in self.points][:-(len(self.points) - numPoints)]
        ydata = [point[1] for point in self.points][:-(len(self.points) - numPoints)]
        data = self.np.column_stack((xdata, ydata))
        
        # Clustering
        clusters = hcluster.fclusterdata(data, thresh, criterion="distance")

        # Plotting
        self.plt.scatter(*self.np.transpose(data), c=clusters)
        title = "Clustering: Threshold: %f, Number of clusters: %d" % (round(thresh,3), len(set(clusters)))
        self.plt.title(title)
        self.plt.show()        


if __name__ == "__main__":
    import time
    startTime = time.time()

    obj = GCodeParser(fileName='TestData/other-test-gcode.gcode', allPoints=False, maxRuns=100000)
    totalTime = round(time.time() - startTime, 3)
    print('Runtime =', totalTime, 'seconds')

    obj.graph3D()
    obj.cluster2D()
